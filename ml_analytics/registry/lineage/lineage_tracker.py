from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime
import networkx as nx

class LineageTracker:
    def __init__(self, registry_path: Path):
        self.lineage_path = registry_path / "lineage"
        self.lineage_path.mkdir(parents=True, exist_ok=True)
        self.graph = nx.DiGraph()
        self._load_existing_lineage()
        
    def _load_existing_lineage(self):
        """Load existing lineage data"""
        if (self.lineage_path / "lineage_graph.json").exists():
            with open(self.lineage_path / "lineage_graph.json", 'r') as f:
                data = json.load(f)
                self.graph.add_edges_from(data["edges"])
                
    def track_model_lineage(self, model_id: str, parent_id: Optional[str], metadata: Dict[str, Any]) -> None:
        """Track model lineage information"""
        self.graph.add_node(model_id, **metadata)
        if parent_id:
            self.graph.add_edge(parent_id, model_id)
            
        self._save_lineage()
        
    def get_model_ancestry(self, model_id: str) -> Dict[str, Any]:
        """Get model's complete ancestry"""
        if model_id not in self.graph:
            return {}
            
        ancestors = list(nx.ancestors(self.graph, model_id))
        descendants = list(nx.descendants(self.graph, model_id))
        
        return {
            "ancestors": ancestors,
            "descendants": descendants,
            "immediate_parent": list(self.graph.predecessors(model_id)),
            "children": list(self.graph.successors(model_id))
        } 