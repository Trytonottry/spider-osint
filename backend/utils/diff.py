# utils/diff.py
import json
from typing import Dict, List

def compare_results(old_ dict, new_ dict) -> Dict[str, List[str]]:
    changes = {}
    
    for module in new_:
        old_module = old_data.get(module, {})
        new_module = new_data.get(module, {})
        
        if json.dumps(old_module, sort_keys=True) != json.dumps(new_module, sort_keys=True):
            changes[module] = [
                f"Изменено: {module}",
                f"Было: {truncate(str(old_module), 100)}",
                f"Стало: {truncate(str(new_module), 100)}"
            ]
    
    return changes

def truncate(text: str, length: int) -> str:
    return text[:length] + "..." if len(text) > length else text