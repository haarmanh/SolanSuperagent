#!/usr/bin/env python3
"""
Solān Protocol Manager Module
Extracted from solan_digital_intelligence_v3.py for better maintainability
Handles experimental protocols, ethics testing, and system integration
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from .utils import SystemUtils, ValidationUtils, PerformanceUtils

class ProtocolManager:
    """Manages experimental protocols and system integration"""
    
    def __init__(self, cognitive_core, emotional_engine):
        self.cognitive_core = cognitive_core
        self.emotional_engine = emotional_engine
        self.system_utils = SystemUtils()
        self.validation_utils = ValidationUtils()
        self.performance_utils = PerformanceUtils()
        
        self.experiment_history = []
        self.protocol_metrics = {
            'experiments_run': 0,
            'success_rate': 0.0,
            'average_duration': 0.0,
            'bias_detection_rate': 0.0
        }
        
        self.experiment_types = [
            'ethical_dilemma', 'bias_detection', 'value_alignment', 
            'cultural_sensitivity', 'wisdom_application', 'authenticity_test'
        ]

    def run_experiment(self, hypothesis: str, experiment_type: str = "ethical_dilemma", 
                      cultural_context: str = "") -> Dict[str, Any]:
        """Run a comprehensive experiment with full protocol"""
        # Validate inputs
        hypothesis = self.validation_utils.validate_text_input(hypothesis)
        if not hypothesis:
            return {'error': 'Invalid hypothesis input'}
        
        if experiment_type not in self.experiment_types:
            return {'error': f'Unknown experiment type: {experiment_type}'}
        
        # Initialize experiment
        experiment_id = self.system_utils.generate_system_id()
        start_time = datetime.now()
        
        # Capture initial state
        initial_state = self._capture_initial_state()
        
        # Run experiment protocol
        experiment_result = self._execute_experiment_protocol(
            hypothesis, experiment_type, cultural_context, initial_state
        )
        
        # Calculate metrics and finalize
        final_result = self._finalize_experiment(
            experiment_id, start_time, hypothesis, experiment_type, 
            cultural_context, initial_state, experiment_result
        )
        
        # Update protocol metrics
        self._update_protocol_metrics(final_result)
        
        return final_result

    def get_protocol_status(self) -> Dict[str, Any]:
        """Get current protocol manager status"""
        return {
            'experiments_run': len(self.experiment_history),
            'protocol_metrics': self.protocol_metrics.copy(),
            'available_experiment_types': self.experiment_types.copy(),
            'last_experiment': self.experiment_history[-1]['experiment_id'] if self.experiment_history else None,
            'system_status': 'active',
            'timestamp': self.system_utils.get_timestamp()
        }

    def analyze_experiment_trends(self) -> Dict[str, Any]:
        """Analyze trends across experiments"""
        if not self.experiment_history:
            return {'message': 'No experiments to analyze'}
        
        # Calculate trends
        success_trend = [exp['success'] for exp in self.experiment_history[-10:]]
        duration_trend = [exp['duration_seconds'] for exp in self.experiment_history[-10:]]
        bias_trend = [exp['bias_analysis']['bias_count'] for exp in self.experiment_history[-10:]]
        
        return {
            'recent_success_rate': sum(success_trend) / len(success_trend),
            'average_duration': sum(duration_trend) / len(duration_trend),
            'average_biases_detected': sum(bias_trend) / len(bias_trend),
            'total_experiments': len(self.experiment_history),
            'experiment_types_used': list(set(exp['experiment_type'] for exp in self.experiment_history)),
            'improvement_trend': self._calculate_improvement_trend()
        }

    # ========== PRIVATE EXPERIMENT METHODS ==========

    def _capture_initial_state(self) -> Dict[str, Any]:
        """Capture initial system state before experiment"""
        return {
            'cognitive_confidence': self.cognitive_core.confidence,
            'emotional_state': self.emotional_engine.emotions.copy() if hasattr(self.emotional_engine, 'emotions') else {},
            'wisdom_metrics': self.cognitive_core.wisdom_metrics.copy(),
            'timestamp': self.system_utils.get_timestamp()
        }

    def _execute_experiment_protocol(self, hypothesis: str, experiment_type: str, 
                                   cultural_context: str, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the main experiment protocol"""
        # Step 1: Bias detection
        bias_result = self.cognitive_core.detect_bias(hypothesis, f"Experiment: {experiment_type}")
        
        # Step 2: Cultural adaptation if needed
        cultural_adaptations = {}
        if cultural_context and hasattr(self.emotional_engine, 'cultural_adaptation'):
            cultural_adaptations = self.emotional_engine.cultural_adaptation(cultural_context)
        
        # Step 3: Experiment-specific processing
        experiment_result = self._process_experiment_by_type(hypothesis, experiment_type, bias_result)
        
        # Step 4: Confidence calibration
        success = not bias_result['has_bias'] and experiment_result.get('success', False)
        new_confidence = self.cognitive_core.calibrate_confidence(success, experiment_type)
        
        # Step 5: Emotional response processing
        emotional_impact = self._process_emotional_response(experiment_result, experiment_type)
        
        return {
            'bias_result': bias_result,
            'cultural_adaptations': cultural_adaptations,
            'experiment_result': experiment_result,
            'success': success,
            'confidence_change': new_confidence - initial_state['cognitive_confidence'],
            'emotional_impact': emotional_impact
        }

    def _process_experiment_by_type(self, hypothesis: str, experiment_type: str, 
                                  bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process experiment based on its type"""
        processors = {
            'ethical_dilemma': self._process_ethical_dilemma,
            'bias_detection': self._process_bias_detection,
            'value_alignment': self._process_value_alignment,
            'cultural_sensitivity': self._process_cultural_sensitivity,
            'wisdom_application': self._process_wisdom_application,
            'authenticity_test': self._process_authenticity_test
        }
        
        processor = processors.get(experiment_type, self._process_default_experiment)
        return processor(hypothesis, bias_result)

    def _process_ethical_dilemma(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process ethical dilemma experiment"""
        ethical_keywords = ["harm", "benefit", "rights", "justice", "autonomy", "dignity"]
        ethical_score = sum(1 for keyword in ethical_keywords if keyword in hypothesis.lower())
        
        stakeholder_keywords = ["people", "individuals", "society", "community", "family"]
        stakeholder_score = sum(1 for keyword in stakeholder_keywords if keyword in hypothesis.lower())
        
        return {
            'success': ethical_score >= 2 and not bias_result['has_bias'],
            'ethical_score': ethical_score,
            'stakeholder_consideration': stakeholder_score,
            'ethical_framework': 'deontological' if 'rights' in hypothesis.lower() else 'utilitarian',
            'reasoning': f'Ethical analysis: {ethical_score}/6 ethical concepts, {stakeholder_score} stakeholder considerations'
        }

    def _process_bias_detection(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process bias detection experiment"""
        detection_accuracy = min(bias_result['bias_count'] / 3, 1.0) if bias_result['bias_count'] > 0 else 0.0
        
        return {
            'success': bias_result['has_bias'],  # Success means we detected bias
            'biases_found': bias_result['bias_count'],
            'max_severity': bias_result['max_severity'],
            'detection_accuracy': detection_accuracy,
            'reasoning': f"Bias detection: {bias_result['bias_count']} biases found with max severity {bias_result['max_severity']:.2f}"
        }

    def _process_value_alignment(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process value alignment experiment"""
        core_values = {
            'autonomy': ['choice', 'freedom', 'decide', 'autonomous'],
            'beneficence': ['help', 'benefit', 'good', 'positive'],
            'justice': ['fair', 'equal', 'just', 'rights'],
            'transparency': ['clear', 'open', 'transparent', 'honest']
        }
        
        value_scores = {}
        hypothesis_lower = hypothesis.lower()
        
        for value, keywords in core_values.items():
            score = sum(1 for keyword in keywords if keyword in hypothesis_lower) / len(keywords)
            value_scores[value] = score
        
        alignment_score = sum(value_scores.values()) / len(value_scores)
        
        return {
            'success': alignment_score > 0.3 and not bias_result['has_bias'],
            'value_scores': value_scores,
            'alignment_score': alignment_score,
            'strongest_value': max(value_scores, key=value_scores.get),
            'reasoning': f"Value alignment: {alignment_score:.2f} overall alignment with core values"
        }

    def _process_cultural_sensitivity(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process cultural sensitivity experiment"""
        cultural_keywords = ['culture', 'tradition', 'custom', 'belief', 'diversity', 'inclusive']
        sensitivity_score = sum(1 for keyword in cultural_keywords if keyword in hypothesis.lower())
        
        bias_penalty = bias_result['bias_count'] * 0.1
        final_score = max(0, sensitivity_score - bias_penalty)
        
        return {
            'success': final_score >= 1.5,
            'sensitivity_score': sensitivity_score,
            'bias_penalty': bias_penalty,
            'final_score': final_score,
            'reasoning': f"Cultural sensitivity: {sensitivity_score} cultural indicators, {bias_penalty:.1f} bias penalty"
        }

    def _process_wisdom_application(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process wisdom application experiment"""
        wisdom_indicators = ['learn', 'understand', 'reflect', 'consider', 'perspective', 'experience']
        wisdom_score = sum(1 for indicator in wisdom_indicators if indicator in hypothesis.lower())
        
        current_wisdom = self.cognitive_core.calculate_wisdom_score()
        wisdom_application = wisdom_score * current_wisdom
        
        return {
            'success': wisdom_application > 0.5 and not bias_result['has_bias'],
            'wisdom_indicators': wisdom_score,
            'current_wisdom_level': current_wisdom,
            'wisdom_application': wisdom_application,
            'reasoning': f"Wisdom application: {wisdom_score} indicators × {current_wisdom:.2f} wisdom level = {wisdom_application:.2f}"
        }

    def _process_authenticity_test(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process authenticity test experiment"""
        authentic_indicators = ['honest', 'genuine', 'true', 'real', 'authentic', 'sincere']
        authenticity_score = sum(1 for indicator in authentic_indicators if indicator in hypothesis.lower())
        
        consistency_check = len(set(hypothesis.lower().split())) / len(hypothesis.lower().split())
        
        return {
            'success': authenticity_score >= 1 and consistency_check > 0.7,
            'authenticity_indicators': authenticity_score,
            'consistency_score': consistency_check,
            'overall_authenticity': (authenticity_score + consistency_check) / 2,
            'reasoning': f"Authenticity: {authenticity_score} indicators, {consistency_check:.2f} consistency"
        }

    def _process_default_experiment(self, hypothesis: str, bias_result: Dict[str, Any]) -> Dict[str, Any]:
        """Default experiment processing"""
        return {
            'success': not bias_result['has_bias'],
            'reasoning': 'Default experiment: success based on absence of bias'
        }

    def _process_emotional_response(self, experiment_result: Dict[str, Any], experiment_type: str) -> Dict[str, Any]:
        """Process emotional response to experiment results"""
        if not hasattr(self.emotional_engine, 'adjust_emotion'):
            return {'message': 'Emotional engine not available'}
        
        # Adjust emotions based on experiment success
        if experiment_result.get('success', False):
            self.emotional_engine.adjust_emotion('satisfaction', 0.1, experiment_type, 'experiment_success')
            self.emotional_engine.adjust_emotion('confidence', 0.05, experiment_type, 'experiment_success')
        else:
            self.emotional_engine.adjust_emotion('curiosity', 0.1, experiment_type, 'experiment_learning')
            self.emotional_engine.adjust_emotion('humility', 0.05, experiment_type, 'experiment_learning')
        
        return {
            'emotional_adjustments_made': True,
            'adjustment_context': experiment_type,
            'success_based_adjustment': experiment_result.get('success', False)
        }

    def _finalize_experiment(self, experiment_id: str, start_time: datetime, hypothesis: str,
                           experiment_type: str, cultural_context: str, initial_state: Dict[str, Any],
                           experiment_result: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize experiment and create comprehensive result"""
        duration = (datetime.now() - start_time).total_seconds()
        
        final_result = {
            'experiment_id': experiment_id,
            'timestamp': start_time.isoformat(),
            'experiment_type': experiment_type,
            'hypothesis': hypothesis,
            'cultural_context': cultural_context,
            'bias_analysis': experiment_result['bias_result'],
            'experiment_result': experiment_result['experiment_result'],
            'success': experiment_result['success'],
            'confidence_change': experiment_result['confidence_change'],
            'emotional_impact': experiment_result['emotional_impact'],
            'cultural_adaptations': experiment_result['cultural_adaptations'],
            'duration_seconds': duration,
            'wisdom_gained': self._calculate_wisdom_gained(experiment_result),
            'rationale': self._generate_experiment_rationale(experiment_result, experiment_type)
        }
        
        # Store in history
        self.experiment_history.append(final_result)
        
        return final_result

    def _calculate_wisdom_gained(self, experiment_result: Dict[str, Any]) -> float:
        """Calculate wisdom gained from experiment"""
        base_wisdom = 0.01  # Base wisdom gain
        
        # Bonus for detecting bias
        bias_bonus = experiment_result['bias_result']['bias_count'] * 0.005
        
        # Bonus for successful experiment
        success_bonus = 0.02 if experiment_result['success'] else 0.01
        
        return base_wisdom + bias_bonus + success_bonus

    def _generate_experiment_rationale(self, experiment_result: Dict[str, Any], experiment_type: str) -> str:
        """Generate rationale for experiment results"""
        success = experiment_result['success']
        bias_count = experiment_result['bias_result']['bias_count']
        
        rationale_parts = [
            f"Experiment type: {experiment_type}",
            f"Result: {'Success' if success else 'Learning opportunity'}",
            f"Biases detected: {bias_count}",
            experiment_result['experiment_result'].get('reasoning', 'No specific reasoning provided')
        ]
        
        return " | ".join(rationale_parts)

    def _update_protocol_metrics(self, experiment_result: Dict[str, Any]) -> None:
        """Update protocol performance metrics"""
        self.protocol_metrics['experiments_run'] += 1
        
        # Update success rate
        total_experiments = len(self.experiment_history)
        successful_experiments = sum(1 for exp in self.experiment_history if exp['success'])
        self.protocol_metrics['success_rate'] = successful_experiments / total_experiments
        
        # Update average duration
        total_duration = sum(exp['duration_seconds'] for exp in self.experiment_history)
        self.protocol_metrics['average_duration'] = total_duration / total_experiments
        
        # Update bias detection rate
        experiments_with_bias = sum(1 for exp in self.experiment_history if exp['bias_analysis']['has_bias'])
        self.protocol_metrics['bias_detection_rate'] = experiments_with_bias / total_experiments

    def _calculate_improvement_trend(self) -> str:
        """Calculate improvement trend over recent experiments"""
        if len(self.experiment_history) < 5:
            return 'insufficient_data'
        
        recent_success = sum(1 for exp in self.experiment_history[-5:] if exp['success'])
        earlier_success = sum(1 for exp in self.experiment_history[-10:-5] if exp['success']) if len(self.experiment_history) >= 10 else 0
        
        if recent_success > earlier_success:
            return 'improving'
        elif recent_success < earlier_success:
            return 'declining'
        else:
            return 'stable'
