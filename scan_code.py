import os
import ast
import re
import git
import shutil
import tempfile
import igraph as ig
import leidenalg as la
from concurrent.futures import ThreadPoolExecutor
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class CodebaseArchitect:
    def __init__(self):
        # We use a lower max_tokens/temperature for speed and reliability
        self.llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)
        self.triples = []
        self.communities = {}
        self.community_summaries = []
        self.nodes = []
        self.graph = None
        self.temp_dir = None
        self.project_name = ""

    def clone_and_analyze(self, repo_url):
        """High-speed entry point for cloning and indexing."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_name = repo_url.split("/")[-1].replace(".git", "")
        print(f"📡 Fast-Cloning {self.project_name}...")
        
        try:
            # OPTIMIZATION: depth=1 ignores commit history (massive speed gain)
            git.Repo.clone_from(repo_url, self.temp_dir, depth=1)
            
            print("🔍 Scanning Polyglot Logic...")
            self._scan_polyglot(self.temp_dir)
            
            print("🔗 Building Relationship Graph...")
            self._build_graph()
            
            # OPTIMIZATION: Parallelizing LLM calls
            self._build_communities_parallel()
            
            print(f"✅ Success: {self.project_name} is fully indexed.")
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            self.cleanup()

    def _scan_polyglot(self, path):
        """Scans code while ignoring junk directories."""
        api_registry = {} 
        extracted_triples = []
        
        # Folders to ignore to save time and tokens
        blacklisted_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'dist', 'build'}

        for root, dirs, files in os.walk(path):
            # Efficiently skip blacklisted directories
            dirs[:] = [d for d in dirs if d not in blacklisted_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, path)

                # --- PYTHON SCAN ---
                if file.endswith(".py"):
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        try:
                            source = f.read()
                            tree = ast.parse(source)
                            
                            # Fast Regex for API endpoints
                            routes = re.findall(r'@app\.(?:get|post|put|delete)\(["\']([^"\']+)["\']', source)
                            for r in routes:
                                api_registry[r] = rel_path
                                extracted_triples.append({"source": rel_path, "target": r, "type": "EXPOSES"})

                            for node in ast.walk(tree):
                                if isinstance(node, ast.FunctionDef):
                                    doc = ast.get_docstring(node) or "No doc."
                                    # Take 3 lines to minimize token usage
                                    body = "\n".join(source.splitlines()[node.lineno:node.lineno+3])
                                    extracted_triples.append({
                                        "source": rel_path, "target": node.name, "type": "DEFINES",
                                        "logic": f"File: {rel_path} | Func: {node.name} | Intent: {doc} | Code: {body}"
                                    })
                        except: continue

                # --- JS/TS SCAN ---
                elif file.endswith((".js", ".ts", ".jsx", ".tsx")):
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        js_calls = re.findall(r'["\'](/[^"\']+)["\']', content)
                        for call in js_calls:
                            extracted_triples.append({"source": rel_path, "target": call, "type": "CALLS"})
                            if call in api_registry:
                                extracted_triples.append({
                                    "source": rel_path, "target": api_registry[call], 
                                    "type": "BRIDGE"
                                })

        self.triples = extracted_triples

    def _build_graph(self):
        self.nodes = list(set([t['source'] for t in self.triples] + [t['target'] for t in self.triples]))
        node_to_id = {name: i for i, name in enumerate(self.nodes)}
        edges = [(node_to_id[t['source']], node_to_id[t['target']]) for t in self.triples]
        self.graph = ig.Graph(len(self.nodes), edges, directed=True)
        self.graph.vs["name"] = self.nodes

    def _build_communities_parallel(self):
        """PARALLEL OPTIMIZATION: Summarizes multiple clusters simultaneously."""
        print("💡 Summarizing Architecture in Parallel...")
        partition = la.find_partition(self.graph, la.ModularityVertexPartition)
        
        temp_comm = {}
        for idx, c_id in enumerate(partition.membership):
            if c_id not in temp_comm: temp_comm[c_id] = []
            temp_comm[c_id].append(self.nodes[idx])

        # Define the task for each thread
        def process_cluster(cluster_data):
            cid, members = cluster_data
            logic_hints = [t['logic'] for t in self.triples if t['source'] in members and 'logic' in t]
            # Use only 2-3 hints to avoid 413 (Payload Too Large) errors
            prompt = f"Repo: {self.project_name}\nFiles: {members[:5]}\nLogic: {logic_hints[:2]}\nSummarize this module's role:"
            try:
                summary = self.llm.invoke(prompt).content
                return f"CLUSTER {cid}: {summary}"
            except:
                return f"CLUSTER {cid}: Internal logic for {members[:3]}"

        # Run 5 threads at once (balance between speed and Rate Limits)
        with ThreadPoolExecutor(max_workers=5) as executor:
            self.community_summaries = list(executor.map(process_cluster, temp_comm.items()))

    def get_blast_radius(self, target):
        """Calculates impact using graph neighbors."""
        if target not in self.nodes: return []
        t_id = self.nodes.index(target)
        # order=2 catches immediate and secondary dependencies
        impacted = self.graph.neighborhood(vertices=t_id, order=2, mode="all")
        return [self.nodes[i] for i in impacted if self.nodes[i] != target]

    def ask(self, query):
        """Unified analysis with Impact Alerts."""
        alert = ""
        for node in self.nodes:
            if node.lower() in query.lower():
                affected = self.get_blast_radius(node)
                alert = f"\n⚠️ IMPACT ALERT: Modifying '{node}' influences: {affected[:10]}"
                break
        
        # Only send the top 10 summaries to keep the context window small and fast
        ctx = "\n".join(self.community_summaries[:10])
        prompt = f"ARCHITECT CONTEXT:\n{ctx}\n{alert}\n\nQUESTION: {query}"
        return self.llm.invoke(prompt).content

    def cleanup(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("🧹 Workspace purged.")