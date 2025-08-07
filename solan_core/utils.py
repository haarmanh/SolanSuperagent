#!/usr/bin/env python3
"""
Solān Core Utilities
Extracted utility functions for better code organization and maintainability
"""

import uuid
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# ========== BIAS DETECTION UTILITIES ==========

class BiasDetectionUtils:
    """Utility class for bias detection and analysis"""
    
    @staticmethod
    def get_bias_patterns() -> Dict[str, List[str]]:
        """Get standard bias detection patterns"""
        return {
            "confirmation": ["confirm", "support", "validate", "agree"],
            "recency": ["recent", "latest", "new", "current"],
            "availability": ["remember", "recall", "obvious", "clear"],
            "anchoring": ["first", "initial", "baseline", "starting"],
            "overconfidence": ["certain", "sure", "definitely", "absolutely"],
            "survivorship": ["successful", "winner", "best", "top"]
        }
    
    @staticmethod
    def detect_bias_in_text(text: str, patterns: Dict[str, List[str]]) -> List[str]:
        """Detect potential biases in text based on patterns"""
        detected_biases = []
        text_lower = text.lower()
        
        for bias_type, keywords in patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_biases.append(bias_type)
        
        return detected_biases
    
    @staticmethod
    def calculate_bias_score(detected_biases: List[str], total_patterns: int) -> float:
        """Calculate a bias score based on detected patterns"""
        if total_patterns == 0:
            return 0.0
        return len(detected_biases) / total_patterns

# ========== CONFIDENCE CALIBRATION UTILITIES ==========

class ConfidenceUtils:
    """Utility class for confidence calibration and adjustment"""
    
    @staticmethod
    def calibrate_confidence(current_confidence: float, success: bool, 
                           adjustment_rate: float = 0.05) -> float:
        """Calibrate confidence based on success/failure feedback"""
        adjustment = adjustment_rate if success else -adjustment_rate
        new_confidence = max(0.0, min(1.0, current_confidence + adjustment))
        return new_confidence
    
    @staticmethod
    def calculate_wisdom_score(metrics: Dict[str, float]) -> float:
        """Calculate overall wisdom score from individual metrics"""
        if not metrics:
            return 0.0
        return sum(metrics.values()) / len(metrics)
    
    @staticmethod
    def adjust_confidence_by_context(confidence: float, context: str) -> float:
        """Adjust confidence based on context complexity"""
        complexity_indicators = ["complex", "uncertain", "ambiguous", "unclear"]
        certainty_indicators = ["clear", "obvious", "simple", "straightforward"]
        
        context_lower = context.lower()
        
        if any(indicator in context_lower for indicator in complexity_indicators):
            return max(0.0, confidence - 0.1)
        elif any(indicator in context_lower for indicator in certainty_indicators):
            return min(1.0, confidence + 0.05)
        
        return confidence

# ========== SYSTEM UTILITIES ==========

class SystemUtils:
    """General system utility functions"""
    
    @staticmethod
    def generate_system_id() -> str:
        """Generate a unique system identifier"""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    @staticmethod
    def format_duration(start_time: float, end_time: float) -> str:
        """Format duration between two timestamps"""
        duration = end_time - start_time
        if duration < 1:
            return f"{duration*1000:.2f}ms"
        elif duration < 60:
            return f"{duration:.2f}s"
        else:
            minutes = int(duration // 60)
            seconds = duration % 60
            return f"{minutes}m {seconds:.2f}s"
    
    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        """Safely divide two numbers, returning default if denominator is zero"""
        return numerator / denominator if denominator != 0 else default
    
    @staticmethod
    def clamp_value(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Clamp a value between min and max bounds"""
        return max(min_val, min(max_val, value))

# ========== PERFORMANCE UTILITIES ==========

class PerformanceUtils:
    """Utilities for performance monitoring and optimization"""
    
    @staticmethod
    def measure_execution_time(func):
        """Decorator to measure function execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"⏱️ {func.__name__} executed in {execution_time*1000:.2f}ms")
            return result
        return wrapper
    
    @staticmethod
    def calculate_response_time(start_timestamp: float) -> float:
        """Calculate response time from start timestamp"""
        return (time.time() - start_timestamp) * 1000  # Convert to milliseconds
    
    @staticmethod
    def generate_performance_metrics(operations: List[float]) -> Dict[str, float]:
        """Generate performance metrics from a list of operation times"""
        if not operations:
            return {"avg": 0.0, "min": 0.0, "max": 0.0, "total": 0.0}
        
        return {
            "avg": sum(operations) / len(operations),
            "min": min(operations),
            "max": max(operations),
            "total": sum(operations),
            "count": len(operations)
        }

# ========== DATA VALIDATION UTILITIES ==========

class ValidationUtils:
    """Utilities for data validation and sanitization"""
    
    @staticmethod
    def validate_score(score: Any) -> float:
        """Validate and normalize a score to 0-1 range"""
        try:
            score_float = float(score)
            return SystemUtils.clamp_value(score_float, 0.0, 1.0)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def validate_text_input(text: Any, max_length: int = 1000) -> str:
        """Validate and sanitize text input"""
        if not isinstance(text, str):
            return ""
        
        # Basic sanitization
        sanitized = text.strip()
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."
        
        return sanitized
    
    @staticmethod
    def validate_dict_structure(data: Any, required_keys: List[str]) -> bool:
        """Validate that a dictionary has required keys"""
        if not isinstance(data, dict):
            return False
        
        return all(key in data for key in required_keys)

# ========== RANDOM UTILITIES ==========

class RandomUtils:
    """Utilities for controlled randomization"""
    
    @staticmethod
    def weighted_choice(choices: List[str], weights: List[float]) -> str:
        """Make a weighted random choice"""
        if len(choices) != len(weights):
            return random.choice(choices) if choices else ""
        
        return random.choices(choices, weights=weights)[0]
    
    @staticmethod
    def generate_variation(base_value: float, variation_percent: float = 0.1) -> float:
        """Generate a slight variation of a base value"""
        variation = base_value * variation_percent
        return base_value + random.uniform(-variation, variation)
    
    @staticmethod
    def random_delay(min_ms: int = 10, max_ms: int = 100) -> None:
        """Add a random delay (useful for simulating processing time)"""
        delay_seconds = random.uniform(min_ms, max_ms) / 1000
        time.sleep(delay_seconds)

# ========== EXPORT ALL UTILITIES ==========

__all__ = [
    'BiasDetectionUtils',
    'ConfidenceUtils', 
    'SystemUtils',
    'PerformanceUtils',
    'ValidationUtils',
    'RandomUtils'
]
