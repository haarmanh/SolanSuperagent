#!/usr/bin/env python3
"""
Solān Cognitive Core Module
Extracted from solan_digital_intelligence_v3.py for better maintainability
Enhanced cognitive processing with bias detection and metacognitive awareness
"""

import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from .utils import BiasDetectionUtils, ConfidenceUtils, ValidationUtils, SystemUtils

class CognitiveCore:
    """Enhanced cognitive core with advanced self-monitoring and bias detection"""
    
    def __init__(self):
        self.memory = []
        self.confidence = 0.75  # Initial confidence in own thinking
        self.biases_detected = []
        self.metacognitive_history = []
        self.wisdom_metrics = {
            'epistemic_humility': 0.7,
            'cognitive_flexibility': 0.6,
            'perspective_taking': 0.8,
            'uncertainty_tolerance': 0.5
        }
        
        # Initialize utility classes
        self.bias_utils = BiasDetectionUtils()
        self.confidence_utils = ConfidenceUtils()
        self.validation_utils = ValidationUtils()
        self.system_utils = SystemUtils()
        
        # Enhanced bias detection patterns
        self.bias_patterns = self.bias_utils.get_bias_patterns()

    def calibrate_confidence(self, success: bool, context: str = "") -> float:
        """Enhanced confidence calibration with metacognitive awareness"""
        # Use utility function for base calibration
        base_adjustment = 0.05 if success else -0.05
        
        # Adjust based on wisdom metrics
        humility_factor = self.wisdom_metrics['epistemic_humility']
        if not success and humility_factor > 0.7:
            base_adjustment *= 1.5  # Learn more from failures when humble
        
        old_confidence = self.confidence
        self.confidence = self.confidence_utils.calibrate_confidence(
            self.confidence, success, abs(base_adjustment)
        )
        
        # Log metacognitive reflection
        self._log_metacognitive_reflection(old_confidence, success, context, base_adjustment)
        
        # Update wisdom metrics
        if not success:
            self._update_wisdom_metric('epistemic_humility', 0.02)
        
        return self.confidence

    def detect_bias(self, hypothesis: str, context: str = "") -> Dict[str, Any]:
        """Enhanced bias detection with pattern matching and severity assessment"""
        # Validate input
        hypothesis = self.validation_utils.validate_text_input(hypothesis)
        if not hypothesis:
            return self._create_empty_bias_result()
        
        # Use utility for bias detection
        detected_biases = self.bias_utils.detect_bias_in_text(hypothesis, self.bias_patterns)
        
        # Calculate detailed bias information
        bias_details = self._calculate_bias_details(hypothesis, detected_biases)
        
        # Create comprehensive result
        bias_result = {
            'has_bias': len(bias_details) > 0,
            'detected_biases': bias_details,
            'bias_count': len(bias_details),
            'max_severity': max([b['severity'] for b in bias_details]) if bias_details else 0,
            'hypothesis': hypothesis,
            'context': context,
            'timestamp': self.system_utils.get_timestamp()
        }
        
        # Store bias detection for learning
        if bias_result['has_bias']:
            self.biases_detected.append(bias_result)
            self._update_wisdom_metric('cognitive_flexibility', 0.01)
        
        return bias_result

    def think_metacognitively(self, thought: str, context: str = "") -> Dict[str, Any]:
        """Enhanced metacognitive thinking with self-reflection"""
        # Validate input
        thought = self.validation_utils.validate_text_input(thought)
        if not thought:
            return {'error': 'Invalid thought input'}
        
        # Analyze the thought process
        bias_analysis = self.detect_bias(thought, context)
        confidence_assessment = self._assess_thought_confidence(thought)
        perspective_analysis = self._analyze_perspectives(thought)
        
        # Generate metacognitive insights
        metacognitive_result = {
            'original_thought': thought,
            'context': context,
            'bias_analysis': bias_analysis,
            'confidence_assessment': confidence_assessment,
            'perspective_analysis': perspective_analysis,
            'wisdom_metrics': self.wisdom_metrics.copy(),
            'recommendations': self._generate_thinking_recommendations(bias_analysis, confidence_assessment),
            'timestamp': self.system_utils.get_timestamp()
        }
        
        # Store for learning
        self.metacognitive_history.append(metacognitive_result)
        
        return metacognitive_result

    def calculate_wisdom_score(self) -> float:
        """Calculate overall wisdom score from individual metrics"""
        return self.confidence_utils.calculate_wisdom_score(self.wisdom_metrics)

    def get_cognitive_state(self) -> Dict[str, Any]:
        """Get current cognitive state summary"""
        return {
            'confidence': self.confidence,
            'wisdom_score': self.calculate_wisdom_score(),
            'wisdom_metrics': self.wisdom_metrics.copy(),
            'total_biases_detected': len(self.biases_detected),
            'metacognitive_entries': len(self.metacognitive_history),
            'memory_size': len(self.memory),
            'last_updated': self.system_utils.get_timestamp()
        }

    # ========== PRIVATE HELPER METHODS ==========

    def _log_metacognitive_reflection(self, old_confidence: float, success: bool, 
                                    context: str, adjustment: float) -> None:
        """Log metacognitive reflection for learning"""
        reflection = {
            'timestamp': datetime.now(),
            'old_confidence': old_confidence,
            'new_confidence': self.confidence,
            'success': success,
            'context': context,
            'adjustment': adjustment
        }
        self.metacognitive_history.append(reflection)

    def _update_wisdom_metric(self, metric_name: str, adjustment: float) -> None:
        """Update a specific wisdom metric"""
        if metric_name in self.wisdom_metrics:
            current_value = self.wisdom_metrics[metric_name]
            new_value = self.system_utils.clamp_value(current_value + adjustment, 0.0, 1.0)
            self.wisdom_metrics[metric_name] = new_value

    def _create_empty_bias_result(self) -> Dict[str, Any]:
        """Create empty bias detection result"""
        return {
            'has_bias': False,
            'detected_biases': [],
            'bias_count': 0,
            'max_severity': 0,
            'hypothesis': '',
            'context': '',
            'timestamp': self.system_utils.get_timestamp()
        }

    def _calculate_bias_details(self, hypothesis: str, detected_biases: List[str]) -> List[Dict[str, Any]]:
        """Calculate detailed information for detected biases"""
        bias_details = []
        hypothesis_lower = hypothesis.lower()
        
        for bias_type in detected_biases:
            if bias_type in self.bias_patterns:
                patterns = self.bias_patterns[bias_type]
                matches = [pattern for pattern in patterns if pattern in hypothesis_lower]
                severity = len(matches) / len(patterns) if patterns else 0
                
                bias_details.append({
                    'type': bias_type,
                    'patterns_matched': matches,
                    'severity': severity,
                    'description': self._get_bias_description(bias_type)
                })
        
        return bias_details

    def _get_bias_description(self, bias_type: str) -> str:
        """Get description for a specific bias type"""
        descriptions = {
            'confirmation': 'Tendency to search for or interpret information that confirms existing beliefs',
            'recency': 'Giving greater weight to recent events or information',
            'availability': 'Overestimating likelihood of events based on how easily examples come to mind',
            'anchoring': 'Heavy reliance on first piece of information encountered',
            'overconfidence': 'Excessive confidence in own answers or abilities',
            'survivorship': 'Focusing on successful examples while overlooking failures'
        }
        return descriptions.get(bias_type, 'Unknown bias type')

    def _assess_thought_confidence(self, thought: str) -> Dict[str, Any]:
        """Assess confidence level for a specific thought"""
        # Simple heuristics for confidence assessment
        uncertainty_indicators = ['maybe', 'perhaps', 'might', 'could', 'possibly']
        certainty_indicators = ['definitely', 'certainly', 'absolutely', 'clearly', 'obviously']
        
        thought_lower = thought.lower()
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in thought_lower)
        certainty_count = sum(1 for indicator in certainty_indicators if indicator in thought_lower)
        
        # Adjust confidence based on context
        base_confidence = self.confidence
        if uncertainty_count > certainty_count:
            adjusted_confidence = max(0.0, base_confidence - 0.1)
        elif certainty_count > uncertainty_count:
            adjusted_confidence = min(1.0, base_confidence + 0.05)
        else:
            adjusted_confidence = base_confidence
        
        return {
            'base_confidence': base_confidence,
            'adjusted_confidence': adjusted_confidence,
            'uncertainty_indicators': uncertainty_count,
            'certainty_indicators': certainty_count,
            'confidence_level': 'high' if adjusted_confidence > 0.8 else 'medium' if adjusted_confidence > 0.5 else 'low'
        }

    def _analyze_perspectives(self, thought: str) -> Dict[str, Any]:
        """Analyze different perspectives present in the thought"""
        perspective_indicators = {
            'self': ['I think', 'I believe', 'my view', 'in my opinion'],
            'others': ['they think', 'others believe', 'people say', 'it is said'],
            'objective': ['research shows', 'evidence suggests', 'data indicates', 'studies prove'],
            'alternative': ['however', 'on the other hand', 'alternatively', 'but']
        }
        
        thought_lower = thought.lower()
        perspectives_found = {}
        
        for perspective_type, indicators in perspective_indicators.items():
            count = sum(1 for indicator in indicators if indicator in thought_lower)
            perspectives_found[perspective_type] = count
        
        total_perspectives = sum(perspectives_found.values())
        perspective_diversity = len([p for p in perspectives_found.values() if p > 0])
        
        return {
            'perspectives_found': perspectives_found,
            'total_perspective_indicators': total_perspectives,
            'perspective_diversity': perspective_diversity,
            'perspective_balance': perspective_diversity / 4.0,  # Normalized to 0-1
            'dominant_perspective': max(perspectives_found, key=perspectives_found.get) if total_perspectives > 0 else 'none'
        }

    def _generate_thinking_recommendations(self, bias_analysis: Dict[str, Any], 
                                         confidence_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving thinking"""
        recommendations = []
        
        # Bias-based recommendations
        if bias_analysis['has_bias']:
            if bias_analysis['bias_count'] > 2:
                recommendations.append("Consider multiple perspectives to reduce cognitive biases")
            
            for bias in bias_analysis['detected_biases']:
                if bias['severity'] > 0.5:
                    recommendations.append(f"Be aware of {bias['type']} bias: {bias['description']}")
        
        # Confidence-based recommendations
        confidence_level = confidence_assessment['confidence_level']
        if confidence_level == 'high' and confidence_assessment['certainty_indicators'] > 2:
            recommendations.append("High confidence detected - consider potential overconfidence")
        elif confidence_level == 'low':
            recommendations.append("Low confidence - seek additional information or perspectives")
        
        # Wisdom metric recommendations
        if self.wisdom_metrics['epistemic_humility'] < 0.5:
            recommendations.append("Practice epistemic humility - acknowledge what you don't know")
        if self.wisdom_metrics['cognitive_flexibility'] < 0.5:
            recommendations.append("Increase cognitive flexibility - consider alternative viewpoints")
        
        return recommendations if recommendations else ["Continue thoughtful analysis"]
