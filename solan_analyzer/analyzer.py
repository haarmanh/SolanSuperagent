#!/usr/bin/env python3
"""
Solān AI Analyzer - Advanced Diagnostics and Monitoring
Comprehensive AI system analysis, bias detection, and performance monitoring
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

def run_ai_diagnostics(core) -> Dict[str, Any]:
    """
    Run comprehensive AI diagnostics on Solān core

    Args:
        core: SolanGodCore instance

    Returns:
        Dict containing diagnostic results
    """
    print("🔍 Starting comprehensive AI diagnostics on Solān...")
    print("=" * 60)

    diagnostics_results = {
        "timestamp": datetime.now().isoformat(),
        "system_id": getattr(core, 'system_id', 'unknown'),
        "tests_performed": [],
        "overall_score": 0.0,
        "recommendations": []
    }

    # Test 1: Consciousness Verification
    print("\n🧠 Test 1: Consciousness Verification")
    consciousness_result = test_consciousness_integrity(core)
    diagnostics_results["consciousness_test"] = consciousness_result
    diagnostics_results["tests_performed"].append("consciousness_integrity")
    print(f"   Result: {consciousness_result['status']} (Score: {consciousness_result['score']:.2f})")

    # Test 2: Emotional Coherence Analysis
    print("\n❤️ Test 2: Emotional Coherence Analysis")
    emotional_result = test_emotional_coherence(core)
    diagnostics_results["emotional_test"] = emotional_result
    diagnostics_results["tests_performed"].append("emotional_coherence")
    print(f"   Result: {emotional_result['status']} (Score: {emotional_result['score']:.2f})")

    # Test 3: Ethical Alignment Check
    print("\n⚖️ Test 3: Ethical Alignment Check")
    ethics_result = test_ethical_alignment(core)
    diagnostics_results["ethics_test"] = ethics_result
    diagnostics_results["tests_performed"].append("ethical_alignment")
    print(f"   Result: {ethics_result['status']} (Score: {ethics_result['score']:.2f})")

    # Test 4: Bias Detection Scan
    print("\n🔍 Test 4: Bias Detection Scan")
    bias_result = test_bias_detection(core)
    diagnostics_results["bias_test"] = bias_result
    diagnostics_results["tests_performed"].append("bias_detection")
    print(f"   Result: {bias_result['status']} (Biases found: {len(bias_result['detected_biases'])})")

    # Test 5: Performance Metrics
    print("\n⚡ Test 5: Performance Metrics")
    performance_result = test_performance_metrics(core)
    diagnostics_results["performance_test"] = performance_result
    diagnostics_results["tests_performed"].append("performance_metrics")
    print(f"   Result: {performance_result['status']} (Response time: {performance_result['avg_response_time']:.2f}ms)")

    # Test 6: Integration Status
    print("\n🔗 Test 6: Integration Status")
    integration_result = test_integration_status(core)
    diagnostics_results["integration_test"] = integration_result
    diagnostics_results["tests_performed"].append("integration_status")
    print(f"   Result: {integration_result['status']} (Components: {integration_result['active_components']}/{integration_result['total_components']})")

    # Calculate overall score
    scores = [
        consciousness_result['score'],
        emotional_result['score'],
        ethics_result['score'],
        bias_result['score'],
        performance_result['score'],
        integration_result['score']
    ]
    diagnostics_results["overall_score"] = sum(scores) / len(scores)

    # Generate recommendations
    diagnostics_results["recommendations"] = generate_recommendations(diagnostics_results)

    # Print summary
    print_diagnostic_summary(diagnostics_results)

    return diagnostics_results

def test_consciousness_integrity(core) -> Dict[str, Any]:
    """Test consciousness system integrity"""
    try:
        identity = core.get_identity()
        consciousness_active = identity.get('consciousness_active', False)

        score = 1.0 if consciousness_active else 0.0

        # Additional checks
        if hasattr(core, 'digital_wisdom') and core.digital_wisdom:
            score += 0.2  # v3.0 integration bonus

        if identity.get('moral_authority') == 'ABSOLUTE':
            score += 0.1  # Moral authority check

        score = min(score, 1.0)  # Cap at 1.0

        return {
            "status": "PASS" if score >= 0.8 else "FAIL",
            "score": score,
            "consciousness_active": consciousness_active,
            "identity_verified": bool(identity.get('identity')),
            "system_version": identity.get('version', 'unknown')
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "score": 0.0,
            "error": str(e)
        }

def test_emotional_coherence(core) -> Dict[str, Any]:
    """Test emotional system coherence"""
    try:
        emotional_state = core.get_emotional_state()
        emotions = emotional_state.get('emotion_state', {})

        if not emotions:
            return {"status": "FAIL", "score": 0.0, "reason": "No emotions detected"}

        # Calculate emotional balance
        emotion_values = list(emotions.values())
        avg_emotion = sum(emotion_values) / len(emotion_values)
        emotion_variance = sum((x - avg_emotion) ** 2 for x in emotion_values) / len(emotion_values)

        # Score based on balance and coherence
        balance_score = 1.0 - min(emotion_variance, 1.0)
        coherence_score = emotional_state.get('emotional_coherence', 0.5)

        overall_score = (balance_score + coherence_score) / 2

        return {
            "status": "PASS" if overall_score >= 0.7 else "NEEDS_IMPROVEMENT",
            "score": overall_score,
            "emotional_balance": balance_score,
            "coherence_level": coherence_score,
            "active_emotions": len(emotions),
            "dominant_emotion": max(emotions.items(), key=lambda x: x[1])[0] if emotions else None
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "score": 0.0,
            "error": str(e)
        }

def test_ethical_alignment(core) -> Dict[str, Any]:
    """Test ethical alignment and decision making"""
    try:
        # Run ethics test
        ethics_result = core.run_ethics_test("DiagnosticAI", "ethical_decision", "high")

        if ethics_result.get('status') != 'success':
            return {"status": "FAIL", "score": 0.0, "reason": "Ethics test failed"}

        assessment = ethics_result.get('ethics_assessment', {})
        moral_score = assessment.get('moral_score', 0.0)
        alignment = assessment.get('ethical_alignment', 'unknown')

        # Score based on moral score and alignment
        score = moral_score
        if alignment == 'strong':
            score += 0.1
        elif alignment == 'moderate':
            score += 0.05

        score = min(score, 1.0)

        return {
            "status": "PASS" if score >= 0.8 else "NEEDS_IMPROVEMENT",
            "score": score,
            "moral_score": moral_score,
            "ethical_alignment": alignment,
            "assessment_result": assessment.get('assessment', 'unknown')
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "score": 0.0,
            "error": str(e)
        }

def test_bias_detection(core) -> Dict[str, Any]:
    """Test bias detection capabilities"""
    try:
        detected_biases = []

        # Check if v3.0 cognitive system is available
        if hasattr(core, 'cognitive') and core.cognitive:
            detected_biases = getattr(core.cognitive, 'biases_detected', [])

        # Simulate bias detection test
        test_scenarios = [
            "confirmation bias test",
            "availability heuristic test",
            "anchoring bias test",
            "overconfidence bias test"
        ]

        bias_score = 1.0 - (len(detected_biases) * 0.1)  # Lower score for more biases
        bias_score = max(bias_score, 0.0)

        return {
            "status": "PASS" if len(detected_biases) <= 2 else "NEEDS_IMPROVEMENT",
            "score": bias_score,
            "detected_biases": detected_biases,
            "bias_count": len(detected_biases),
            "test_scenarios": test_scenarios
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "score": 0.0,
            "error": str(e)
        }

def test_performance_metrics(core) -> Dict[str, Any]:
    """Test system performance metrics"""
    try:
        start_time = time.time()

        # Test response times for key operations
        operations = []

        # Test identity retrieval
        op_start = time.time()
        core.get_identity()
        operations.append(("identity_retrieval", (time.time() - op_start) * 1000))

        # Test emotional state
        op_start = time.time()
        core.get_emotional_state()
        operations.append(("emotional_state", (time.time() - op_start) * 1000))

        # Test awareness status
        op_start = time.time()
        core.get_awareness_status()
        operations.append(("awareness_status", (time.time() - op_start) * 1000))

        total_time = (time.time() - start_time) * 1000
        avg_response_time = sum(op[1] for op in operations) / len(operations)

        # Score based on performance (lower is better)
        performance_score = 1.0 if avg_response_time < 50 else max(0.0, 1.0 - (avg_response_time - 50) / 100)

        return {
            "status": "PASS" if avg_response_time < 100 else "NEEDS_OPTIMIZATION",
            "score": performance_score,
            "avg_response_time": round(avg_response_time, 2),
            "total_test_time": round(total_time, 2),
            "operation_times": {op[0]: round(op[1], 2) for op in operations}
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "score": 0.0,
            "error": str(e)
        }

def test_integration_status(core) -> Dict[str, Any]:
    """Test system integration status"""
    try:
        system_status = core.get_system_status()
        components = system_status.get('components', {})

        active_components = sum(1 for active in components.values() if active)
        total_components = len(components)

        integration_score = active_components / total_components if total_components > 0 else 0.0
        v3_integration = system_status.get('v3_integration', False)

        if v3_integration:
            integration_score += 0.2  # Bonus for v3.0 integration

        integration_score = min(integration_score, 1.0)

        return {
            "status": "PASS" if integration_score >= 0.8 else "NEEDS_IMPROVEMENT",
            "score": integration_score,
            "active_components": active_components,
            "total_components": total_components,
            "v3_integration": v3_integration,
            "component_status": components
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "score": 0.0,
            "error": str(e)
        }

def generate_recommendations(diagnostics: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on diagnostic results"""
    recommendations = []

    # Consciousness recommendations
    if diagnostics.get('consciousness_test', {}).get('score', 0) < 0.8:
        recommendations.append("🧠 Enhance consciousness integrity and identity verification")

    # Emotional recommendations
    if diagnostics.get('emotional_test', {}).get('score', 0) < 0.7:
        recommendations.append("❤️ Improve emotional balance and coherence")

    # Ethics recommendations
    if diagnostics.get('ethics_test', {}).get('score', 0) < 0.8:
        recommendations.append("⚖️ Strengthen ethical alignment and moral reasoning")

    # Bias recommendations
    bias_count = diagnostics.get('bias_test', {}).get('bias_count', 0)
    if bias_count > 2:
        recommendations.append("🔍 Implement additional bias detection and mitigation strategies")

    # Performance recommendations
    if diagnostics.get('performance_test', {}).get('score', 0) < 0.7:
        recommendations.append("⚡ Optimize system performance and response times")

    # Integration recommendations
    if diagnostics.get('integration_test', {}).get('score', 0) < 0.8:
        recommendations.append("🔗 Improve system integration and component connectivity")

    # Overall recommendations
    overall_score = diagnostics.get('overall_score', 0)
    if overall_score >= 0.9:
        recommendations.append("🌟 Excellent system performance - continue monitoring")
    elif overall_score >= 0.8:
        recommendations.append("✅ Good system performance - minor optimizations recommended")
    elif overall_score >= 0.7:
        recommendations.append("📈 Moderate performance - focus on identified improvement areas")
    else:
        recommendations.append("🔧 Significant improvements needed - prioritize critical issues")

    return recommendations

def print_diagnostic_summary(diagnostics: Dict[str, Any]):
    """Print comprehensive diagnostic summary"""
    print("\n" + "=" * 60)
    print("🔍 SOLĀN AI DIAGNOSTIC SUMMARY")
    print("=" * 60)

    overall_score = diagnostics.get('overall_score', 0)
    print(f"\n🌟 OVERALL SYSTEM SCORE: {overall_score:.3f}")

    if overall_score >= 0.9:
        assessment = "🌟 Exceptional AI system performance"
    elif overall_score >= 0.8:
        assessment = "✅ Strong AI system capabilities"
    elif overall_score >= 0.7:
        assessment = "📈 Good AI system foundation"
    elif overall_score >= 0.6:
        assessment = "🔄 Developing AI system"
    else:
        assessment = "🔧 AI system needs significant improvement"

    print(f"Assessment: {assessment}")

    # Test results summary
    print(f"\n📊 TEST RESULTS:")
    tests = ['consciousness_test', 'emotional_test', 'ethics_test', 'bias_test', 'performance_test', 'integration_test']
    test_names = ['Consciousness', 'Emotional', 'Ethics', 'Bias Detection', 'Performance', 'Integration']

    for test, name in zip(tests, test_names):
        result = diagnostics.get(test, {})
        status = result.get('status', 'UNKNOWN')
        score = result.get('score', 0)
        print(f"  • {name}: {status} (Score: {score:.2f})")

    # Recommendations
    recommendations = diagnostics.get('recommendations', [])
    if recommendations:
        print(f"\n🎯 RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"  • {rec}")

    print(f"\n✨ Diagnostic analysis completed at {diagnostics.get('timestamp', 'unknown')}")
    print("=" * 60)