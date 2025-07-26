# infrastructure/monitoring/simple_metrics.py
from datetime import datetime
from collections import defaultdict, deque

class SimpleMetrics:
    def __init__(self, max_history=100):
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=max_history)
        self.requests_by_endpoint = defaultdict(int)
        self.last_requests = deque(maxlen=max_history)
    
    def record_request(self, endpoint, status_code, response_time):
        self.request_count += 1
        self.requests_by_endpoint[endpoint] += 1
        self.response_times.append(response_time)
        
        if status_code >= 400:
            self.error_count += 1
        
        self.last_requests.append({
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time": response_time
        })
    
    def get_metrics(self):
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / self.request_count if self.request_count > 0 else 0,
            "average_response_time": avg_response_time,
            "requests_by_endpoint": dict(self.requests_by_endpoint),
            "recent_requests": list(self.last_requests)
        }

# Create a singleton instance
metrics = SimpleMetrics()