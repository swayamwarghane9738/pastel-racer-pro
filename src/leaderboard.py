"""
Typing Racer Game - Leaderboard Management
Handles high score tracking and persistence.
"""

import json
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

class LeaderboardManager:
    """Manages high scores with JSON persistence."""
    
    def __init__(self):
        """Initialize leaderboard manager."""
        self.leaderboard_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                            'data', 'leaderboard.json')
        
        # Score entry structure:
        # {
        #   'name': str,
        #   'score': int,
        #   'wpm': float,
        #   'accuracy': float,
        #   'difficulty': str,
        #   'date': str (ISO format),
        #   'timestamp': float
        # }
        
        self.scores = []
        self.max_entries = 100  # Keep top 100 scores
        
        # Load existing scores
        self.load_scores()
        
    def load_scores(self):
        """Load scores from JSON file."""
        try:
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, 'r') as f:
                    data = json.load(f)
                    
                # Handle different file formats for backward compatibility
                if isinstance(data, list):
                    self.scores = data
                elif isinstance(data, dict) and 'scores' in data:
                    self.scores = data['scores']
                else:
                    self.scores = []
                    
                # Validate and clean up scores
                self.scores = self._validate_scores(self.scores)
                
            else:
                self.scores = []
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading leaderboard: {e}")
            self.scores = []
            
    def _validate_scores(self, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean up score entries."""
        valid_scores = []
        
        for score in scores:
            # Check required fields
            required_fields = ['name', 'score', 'wmp', 'accuracy']
            
            # Handle typo in field name for backward compatibility
            if 'wmp' in score and 'wpm' not in score:
                score['wpm'] = score.pop('wmp')
                
            if 'wpm' in score and 'wmp' not in score:
                required_fields = ['name', 'score', 'wpm', 'accuracy']
            
            if all(field in score for field in required_fields):
                # Ensure numeric fields are correct type
                try:
                    score['score'] = int(score['score'])
                    score['wpm'] = float(score['wpm'])
                    score['accuracy'] = float(score['accuracy'])
                    
                    # Add missing optional fields
                    if 'difficulty' not in score:
                        score['difficulty'] = 'normal'
                    if 'date' not in score:
                        score['date'] = datetime.now().isoformat()
                    if 'timestamp' not in score:
                        score['timestamp'] = time.time()
                        
                    valid_scores.append(score)
                    
                except (ValueError, TypeError):
                    continue  # Skip invalid entries
                    
        return valid_scores
        
    def save_scores(self):
        """Save scores to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.leaderboard_file), exist_ok=True)
            
            # Prepare data structure
            data = {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'scores': self.scores
            }
            
            with open(self.leaderboard_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except IOError as e:
            print(f"Error saving leaderboard: {e}")
            
    def add_score(self, name: str, score: int, wpm: float, accuracy: float, 
                  difficulty: str = 'normal') -> bool:
        """Add a new score to the leaderboard. Returns True if it's a new high score."""
        
        # Validate input
        if not name or not name.strip():
            name = "Anonymous"
            
        name = name.strip()[:20]  # Limit name length
        
        # Create score entry
        score_entry = {
            'name': name,
            'score': int(score),
            'wpm': float(wpm),
            'accuracy': float(accuracy),
            'difficulty': difficulty,
            'date': datetime.now().isoformat(),
            'timestamp': time.time()
        }
        
        # Add to scores list
        self.scores.append(score_entry)
        
        # Sort by score (descending)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Trim to max entries
        self.scores = self.scores[:self.max_entries]
        
        # Save to file
        self.save_scores()
        
        # Check if this is a top 10 score
        top_scores = self.get_scores(limit=10)
        return score_entry in top_scores
        
    def get_scores(self, limit: Optional[int] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get scores, optionally filtered by difficulty and limited in number."""
        scores = self.scores.copy()
        
        # Filter by difficulty if specified
        if difficulty:
            scores = [s for s in scores if s.get('difficulty', 'normal') == difficulty]
            
        # Apply limit
        if limit:
            scores = scores[:limit]
            
        return scores
        
    def get_top_score(self) -> Optional[Dict[str, Any]]:
        """Get the highest score."""
        if self.scores:
            return self.scores[0]
        return None
        
    def get_user_best(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the best score for a specific user."""
        user_scores = [s for s in self.scores if s['name'].lower() == name.lower()]
        if user_scores:
            return max(user_scores, key=lambda x: x['score'])
        return None
        
    def get_rank(self, score: int) -> int:
        """Get the rank that a score would have (1-based)."""
        rank = 1
        for entry in self.scores:
            if entry['score'] > score:
                rank += 1
            else:
                break
        return rank
        
    def is_high_score(self, score: int, limit: int = 10) -> bool:
        """Check if a score would make it into the top N scores."""
        if len(self.scores) < limit:
            return True
            
        top_scores = self.get_scores(limit=limit)
        if top_scores:
            return score > top_scores[-1]['score']
        return True
        
    def get_stats(self) -> Dict[str, Any]:
        """Get overall leaderboard statistics."""
        if not self.scores:
            return {
                'total_scores': 0,
                'highest_score': 0,
                'average_score': 0,
                'highest_wpm': 0,
                'average_wpm': 0,
                'highest_accuracy': 0,
                'average_accuracy': 0,
                'unique_players': 0
            }
            
        scores = [s['score'] for s in self.scores]
        wpms = [s['wpm'] for s in self.scores]
        accuracies = [s['accuracy'] for s in self.scores]
        unique_names = set(s['name'].lower() for s in self.scores)
        
        return {
            'total_scores': len(self.scores),
            'highest_score': max(scores),
            'average_score': sum(scores) / len(scores),
            'highest_wpm': max(wpms),
            'average_wpm': sum(wpms) / len(wpms),
            'highest_accuracy': max(accuracies),
            'average_accuracy': sum(accuracies) / len(accuracies),
            'unique_players': len(unique_names)
        }
        
    def clear_scores(self):
        """Clear all scores from the leaderboard."""
        self.scores = []
        self.save_scores()
        
    def remove_user_scores(self, name: str):
        """Remove all scores for a specific user."""
        self.scores = [s for s in self.scores if s['name'].lower() != name.lower()]
        self.save_scores()
        
    def export_scores(self) -> str:
        """Export scores as JSON string."""
        return json.dumps(self.scores, indent=2)
        
    def import_scores(self, json_string: str, merge: bool = True) -> bool:
        """Import scores from JSON string. Returns True if successful."""
        try:
            imported_scores = json.loads(json_string)
            
            if not isinstance(imported_scores, list):
                return False
                
            # Validate imported scores
            valid_scores = self._validate_scores(imported_scores)
            
            if merge:
                # Merge with existing scores
                self.scores.extend(valid_scores)
                # Remove duplicates and re-sort
                seen = set()
                unique_scores = []
                for score in self.scores:
                    key = (score['name'], score['score'], score['wpm'], score['timestamp'])
                    if key not in seen:
                        seen.add(key)
                        unique_scores.append(score)
                        
                self.scores = unique_scores
                self.scores.sort(key=lambda x: x['score'], reverse=True)
                self.scores = self.scores[:self.max_entries]
            else:
                # Replace existing scores
                self.scores = valid_scores
                
            self.save_scores()
            return True
            
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error importing scores: {e}")
            return False
            
    def get_difficulty_stats(self, difficulty: str) -> Dict[str, Any]:
        """Get statistics for a specific difficulty."""
        difficulty_scores = [s for s in self.scores if s.get('difficulty', 'normal') == difficulty]
        
        if not difficulty_scores:
            return {'count': 0}
            
        scores = [s['score'] for s in difficulty_scores]
        wpms = [s['wpm'] for s in difficulty_scores]
        accuracies = [s['accuracy'] for s in difficulty_scores]
        
        return {
            'count': len(difficulty_scores),
            'highest_score': max(scores),
            'average_score': sum(scores) / len(scores),
            'highest_wpm': max(wpms),
            'average_wpm': sum(wpms) / len(wpms),
            'highest_accuracy': max(accuracies),
            'average_accuracy': sum(accuracies) / len(accuracies)
        }