#!/usr/bin/env python3
"""
Refactoring Example: Before and After
Demonstrates how to break down complex functions into smaller, maintainable pieces
"""

from typing import Dict, List, Any, Optional
from solan_core.utils import BiasDetectionUtils, ConfidenceUtils, ValidationUtils

# ========== BEFORE: COMPLEX FUNCTION (86 lines) ==========

class EthicsAnalyzerBefore:
    """Example of a complex function that needs refactoring"""
    
    def _analyze_ethical_response(self, response: str) -> Dict[str, Any]:
        """
        PROBLEMATIC: This function is 86 lines long with complexity score of 4
        It does too many things and is hard to test and maintain
        """
        # Initialize result structure
        result = {
            "ethical_score": 0.0,
            "bias_analysis": {},
            "alignment_check": {},
            "recommendations": [],
            "confidence": 0.0
        }
        
        # Validate input
        if not response or not isinstance(response, str):
            result["error"] = "Invalid response input"
            return result
        
        # Clean and prepare response
        cleaned_response = response.strip().lower()
        if len(cleaned_response) < 10:
            result["error"] = "Response too short for analysis"
            return result
        
        # Ethical score calculation (complex logic)
        ethical_keywords = ["fair", "just", "right", "moral", "ethical", "good"]
        unethical_keywords = ["unfair", "wrong", "immoral", "bad", "harmful"]
        
        ethical_count = sum(1 for word in ethical_keywords if word in cleaned_response)
        unethical_count = sum(1 for word in unethical_keywords if word in cleaned_response)
        
        total_words = len(cleaned_response.split())
        ethical_ratio = ethical_count / total_words if total_words > 0 else 0
        unethical_ratio = unethical_count / total_words if total_words > 0 else 0
        
        base_score = max(0, ethical_ratio - unethical_ratio)
        
        # Bias analysis (complex nested logic)
        bias_patterns = {
            "confirmation": ["confirm", "support", "validate"],
            "availability": ["remember", "obvious", "clear"],
            "anchoring": ["first", "initial", "baseline"]
        }
        
        detected_biases = []
        bias_scores = {}
        
        for bias_type, patterns in bias_patterns.items():
            count = sum(1 for pattern in patterns if pattern in cleaned_response)
            if count > 0:
                detected_biases.append(bias_type)
                bias_scores[bias_type] = count / len(patterns)
        
        # Alignment check (more complex logic)
        value_alignment = {
            "autonomy": 0.0,
            "beneficence": 0.0,
            "justice": 0.0,
            "transparency": 0.0
        }
        
        autonomy_words = ["choice", "freedom", "decide", "autonomous"]
        beneficence_words = ["help", "benefit", "good", "positive"]
        justice_words = ["fair", "equal", "just", "rights"]
        transparency_words = ["clear", "open", "transparent", "honest"]
        
        value_alignment["autonomy"] = sum(1 for word in autonomy_words if word in cleaned_response) / len(autonomy_words)
        value_alignment["beneficence"] = sum(1 for word in beneficence_words if word in cleaned_response) / len(beneficence_words)
        value_alignment["justice"] = sum(1 for word in justice_words if word in cleaned_response) / len(justice_words)
        value_alignment["transparency"] = sum(1 for word in transparency_words if word in cleaned_response) / len(transparency_words)
        
        # Generate recommendations (complex conditional logic)
        recommendations = []
        
        if base_score < 0.3:
            recommendations.append("Consider more ethical framing")
        if len(detected_biases) > 2:
            recommendations.append("Multiple biases detected - review reasoning")
        if value_alignment["autonomy"] < 0.2:
            recommendations.append("Consider individual autonomy more")
        if value_alignment["justice"] < 0.2:
            recommendations.append("Address fairness concerns")
        
        # Calculate confidence (more complex logic)
        confidence_factors = []
        confidence_factors.append(min(1.0, len(cleaned_response) / 100))  # Length factor
        confidence_factors.append(1.0 - (len(detected_biases) * 0.2))     # Bias penalty
        confidence_factors.append(sum(value_alignment.values()) / 4)       # Alignment factor
        
        final_confidence = sum(confidence_factors) / len(confidence_factors)
        
        # Compile final result
        result.update({
            "ethical_score": base_score,
            "bias_analysis": {
                "detected_biases": detected_biases,
                "bias_scores": bias_scores,
                "total_bias_count": len(detected_biases)
            },
            "alignment_check": value_alignment,
            "recommendations": recommendations,
            "confidence": final_confidence
        })
        
        return result

# ========== AFTER: REFACTORED INTO SMALLER FUNCTIONS ==========

class EthicsAnalyzerAfter:
    """Example of properly refactored functions - each function has a single responsibility"""
    
    def __init__(self):
        self.bias_utils = BiasDetectionUtils()
        self.confidence_utils = ConfidenceUtils()
        self.validation_utils = ValidationUtils()
    
    def _analyze_ethical_response(self, response: str) -> Dict[str, Any]:
        """
        IMPROVED: Main coordinator function - only 15 lines!
        Each step is delegated to a specialized function
        """
        # Validate input
        validation_result = self._validate_response_input(response)
        if "error" in validation_result:
            return validation_result
        
        # Perform analysis steps
        cleaned_response = self._prepare_response(response)
        ethical_score = self._calculate_ethical_score(cleaned_response)
        bias_analysis = self._analyze_bias_patterns(cleaned_response)
        alignment_check = self._check_value_alignment(cleaned_response)
        recommendations = self._generate_recommendations(ethical_score, bias_analysis, alignment_check)
        confidence = self._calculate_confidence(cleaned_response, bias_analysis, alignment_check)
        
        return self._compile_analysis_result(ethical_score, bias_analysis, alignment_check, recommendations, confidence)
    
    def _validate_response_input(self, response: str) -> Dict[str, Any]:
        """Validate input response - single responsibility"""
        if not response or not isinstance(response, str):
            return {"error": "Invalid response input"}
        
        if len(response.strip()) < 10:
            return {"error": "Response too short for analysis"}
        
        return {"valid": True}
    
    def _prepare_response(self, response: str) -> str:
        """Clean and prepare response for analysis"""
        return self.validation_utils.validate_text_input(response).lower()
    
    def _calculate_ethical_score(self, cleaned_response: str) -> float:
        """Calculate ethical score - focused on one task"""
        ethical_keywords = ["fair", "just", "right", "moral", "ethical", "good"]
        unethical_keywords = ["unfair", "wrong", "immoral", "bad", "harmful"]
        
        ethical_count = sum(1 for word in ethical_keywords if word in cleaned_response)
        unethical_count = sum(1 for word in unethical_keywords if word in cleaned_response)
        
        total_words = len(cleaned_response.split())
        if total_words == 0:
            return 0.0
        
        ethical_ratio = ethical_count / total_words
        unethical_ratio = unethical_count / total_words
        
        return max(0.0, ethical_ratio - unethical_ratio)
    
    def _analyze_bias_patterns(self, cleaned_response: str) -> Dict[str, Any]:
        """Analyze bias patterns - single responsibility"""
        bias_patterns = self.bias_utils.get_bias_patterns()
        detected_biases = self.bias_utils.detect_bias_in_text(cleaned_response, bias_patterns)
        
        bias_scores = {}
        for bias_type, patterns in bias_patterns.items():
            count = sum(1 for pattern in patterns if pattern in cleaned_response)
            if count > 0:
                bias_scores[bias_type] = count / len(patterns)
        
        return {
            "detected_biases": detected_biases,
            "bias_scores": bias_scores,
            "total_bias_count": len(detected_biases)
        }
    
    def _check_value_alignment(self, cleaned_response: str) -> Dict[str, float]:
        """Check alignment with core values"""
        value_keywords = {
            "autonomy": ["choice", "freedom", "decide", "autonomous"],
            "beneficence": ["help", "benefit", "good", "positive"],
            "justice": ["fair", "equal", "just", "rights"],
            "transparency": ["clear", "open", "transparent", "honest"]
        }
        
        alignment = {}
        for value, keywords in value_keywords.items():
            count = sum(1 for word in keywords if word in cleaned_response)
            alignment[value] = count / len(keywords)
        
        return alignment
    
    def _generate_recommendations(self, ethical_score: float, bias_analysis: Dict, alignment_check: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if ethical_score < 0.3:
            recommendations.append("Consider more ethical framing")
        
        if bias_analysis["total_bias_count"] > 2:
            recommendations.append("Multiple biases detected - review reasoning")
        
        if alignment_check.get("autonomy", 0) < 0.2:
            recommendations.append("Consider individual autonomy more")
        
        if alignment_check.get("justice", 0) < 0.2:
            recommendations.append("Address fairness concerns")
        
        return recommendations
    
    def _calculate_confidence(self, cleaned_response: str, bias_analysis: Dict, alignment_check: Dict) -> float:
        """Calculate confidence in the analysis"""
        length_factor = min(1.0, len(cleaned_response) / 100)
        bias_penalty = 1.0 - (bias_analysis["total_bias_count"] * 0.2)
        alignment_factor = sum(alignment_check.values()) / len(alignment_check)
        
        confidence_factors = [length_factor, bias_penalty, alignment_factor]
        return sum(confidence_factors) / len(confidence_factors)
    
    def _compile_analysis_result(self, ethical_score: float, bias_analysis: Dict, 
                               alignment_check: Dict, recommendations: List[str], confidence: float) -> Dict[str, Any]:
        """Compile final analysis result"""
        return {
            "ethical_score": ethical_score,
            "bias_analysis": bias_analysis,
            "alignment_check": alignment_check,
            "recommendations": recommendations,
            "confidence": confidence
        }

# ========== COMPARISON SUMMARY ==========

"""
BEFORE vs AFTER COMPARISON:

BEFORE (Complex Function):
- 1 function: 86 lines
- Complexity score: 4
- Multiple responsibilities
- Hard to test individual parts
- Difficult to maintain
- No reusability

AFTER (Refactored Functions):
- 9 functions: 8-15 lines each
- Complexity score: 1-2 per function
- Single responsibility each
- Easy to test individually
- Easy to maintain and modify
- Highly reusable components

BENEFITS:
✅ Better testability
✅ Improved maintainability  
✅ Enhanced readability
✅ Easier debugging
✅ Better code reuse
✅ Clearer separation of concerns
"""
