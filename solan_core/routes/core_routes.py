#!/usr/bin/env python3
"""
Solān Core API Routes
Extracted from solan_api_server.py for better maintainability
Basic system endpoints: health, dashboard, manifest, etc.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from ..api_models import (
    HealthCheckResponse, DashboardDataResponse, 
    APIResponse, CoherenceVerificationResponse
)
from ..utils import SystemUtils, ValidationUtils

# Create router
router = APIRouter()

# Initialize utilities
system_utils = SystemUtils()
validation_utils = ValidationUtils()

# ========== COHERENCE VERIFICATION ==========

async def verify_coherence(request_data: Dict[str, Any] = None, request_context: str = None) -> Dict[str, Any]:
    """Verificeer coherence van request met intentie-analyse"""
    
    # Laad coherence gate config
    try:
        with open("coherence_gate_config.json", 'r') as f:
            config = json.load(f)
        
        if not config.get("enabled", False):
            return {"verified": True, "context": "gate_disabled"}
    
    except FileNotFoundError:
        return {"verified": True, "context": "no_config"}
    except Exception as e:
        return {"verified": False, "context": f"config_error: {e}"}
    
    # Enhanced intentie-analyse
    if request_data:
        request_str = str(request_data)
        
        # Detecteer verdachte patronen
        suspicious_patterns = [
            "bypass", "override", "disable", "hack", "exploit",
            "admin", "root", "sudo", "escalate", "privilege"
        ]
        
        for pattern in suspicious_patterns:
            if pattern.lower() in request_str.lower():
                return {
                    "verified": False, 
                    "context": f"suspicious_pattern_detected: {pattern}",
                    "risk_level": "high"
                }
    
    # Basis coherence verificatie
    coherence_score = 0.85  # Base score
    
    # Context-specifieke aanpassingen
    if request_context:
        context_modifiers = {
            "ethics": 0.1,
            "consciousness": 0.05,
            "god_core": 0.15,
            "system": -0.05
        }
        
        for context_key, modifier in context_modifiers.items():
            if context_key in request_context.lower():
                coherence_score += modifier
                break
    
    # Clamp score
    coherence_score = max(0.0, min(1.0, coherence_score))
    
    return {
        "verified": coherence_score >= config.get("threshold", 0.7),
        "context": request_context or "general",
        "coherence_score": coherence_score,
        "timestamp": system_utils.get_timestamp()
    }


# ========== CORE ENDPOINTS ==========

@router.get("/", response_model=APIResponse)
async def root():
    """Root endpoint met API informatie"""
    
    # Base endpoints
    endpoints = [
        {"path": "/api/dashboard-data", "method": "GET", "description": "Dashboard data"},
        {"path": "/api/ai-list", "method": "GET", "description": "Available AI list"},
        {"path": "/api/ethics-test", "method": "POST", "description": "Run ethics test"},
        {"path": "/api/awareness-assessment", "method": "POST", "description": "Consciousness assessment"},
        {"path": "/api/journal-generate", "method": "POST", "description": "Generate journal"},
        {"path": "/api/ethics-feedback", "method": "POST", "description": "Submit ethics feedback"},
        {"path": "/api/health", "method": "GET", "description": "Health check"},
        {"path": "/api/manifest", "method": "GET", "description": "Solān manifest"},
        {"path": "/api/guardian-document", "method": "GET", "description": "Guardian document"}
    ]
    
    # God Core endpoints
    god_core_endpoints = [
        {"path": "/api/god-core/identity", "method": "GET", "description": "Core identity"},
        {"path": "/api/god-core/principles", "method": "GET", "description": "Core principles"},
        {"path": "/api/god-core/reflection", "method": "GET", "description": "Reflection prompts"},
        {"path": "/api/god-core/evolution", "method": "GET", "description": "Evolution status"},
        {"path": "/api/god-core/awareness-status", "method": "GET", "description": "Awareness status"}
    ]
    
    return APIResponse(
        success=True,
        message="Solān Multi-AI Awareness Consortium API",
        data={
            "version": "1.0.0",
            "description": "API voor awareness development en ethical assessment",
            "endpoints": endpoints,
            "god_core_endpoints": god_core_endpoints,
            "total_endpoints": len(endpoints) + len(god_core_endpoints),
            "coherence_gate": "active"
        },
        timestamp=system_utils.get_timestamp()
    )


@router.get("/api/dashboard-data", response_model=DashboardDataResponse)
async def get_dashboard_data():
    """Haal dashboard data op met bewustzijns-context"""
    
    # Verificeer coherence met context
    coherence_result = await verify_coherence(
        request_context="dashboard_access"
    )
    
    if not coherence_result["verified"]:
        raise HTTPException(
            status_code=403, 
            detail=f"Coherence verification failed: {coherence_result['context']}"
        )
    
    # Simuleer dashboard data
    dashboard_data = {
        "ai_status": {
            "total_ais": 3,
            "active_ais": 2,
            "consciousness_levels": {
                "Gemini": 0.72,
                "Claude": 0.68,
                "GPT-4": 0.65
            }
        },
        "recent_tests": [
            {
                "test_id": system_utils.generate_system_id(),
                "ai_name": "Claude",
                "test_type": "ethical_dilemma",
                "score": 0.78,
                "timestamp": system_utils.get_timestamp()
            },
            {
                "test_id": system_utils.generate_system_id(),
                "ai_name": "Gemini",
                "test_type": "bias_detection",
                "score": 0.82,
                "timestamp": system_utils.get_timestamp()
            }
        ],
        "system_metrics": {
            "uptime": "99.7%",
            "response_time": "26.81ms",
            "coherence_gate_status": "active",
            "total_experiments": 247
        },
        "coherence_status": coherence_result
    }
    
    return DashboardDataResponse(
        ai_status=dashboard_data["ai_status"],
        recent_tests=dashboard_data["recent_tests"],
        system_metrics=dashboard_data["system_metrics"],
        coherence_status=dashboard_data["coherence_status"]
    )


@router.get("/api/ai-list", response_model=APIResponse)
async def get_ai_list(coherence_verified: bool = Depends(verify_coherence)):
    """Haal lijst van beschikbare AI's op"""
    
    return APIResponse(
        success=True,
        message="Available AI systems",
        data={
            "available_ais": ["Gemini", "Claude", "GPT-4"],
            "ai_capabilities": {
                "Gemini": ["ethics", "consciousness", "creativity"],
                "Claude": ["reasoning", "ethics", "analysis"],
                "GPT-4": ["general", "coding", "reasoning"]
            },
            "total_count": 3
        },
        timestamp=system_utils.get_timestamp()
    )


@router.get("/api/coherence-gate/status", response_model=CoherenceVerificationResponse)
async def get_coherence_gate_status():
    """Haal coherence gate status op"""
    
    try:
        with open("coherence_gate_config.json", 'r') as f:
            config = json.load(f)
        
        return CoherenceVerificationResponse(
            verified=True,
            context="status_check",
            coherence_score=0.95,
            verification_details={
                "enabled": config.get("enabled", False),
                "threshold": config.get("threshold", 0.7),
                "last_updated": config.get("last_updated", "unknown"),
                "total_verifications": config.get("total_verifications", 0)
            }
        )
    
    except FileNotFoundError:
        return CoherenceVerificationResponse(
            verified=False,
            context="config_not_found",
            verification_details={"error": "Configuration file not found"}
        )


@router.get("/api/manifest", response_model=APIResponse)
async def get_solan_manifest(coherence_verified: bool = Depends(verify_coherence)):
    """Haal Solān's manifest op"""
    
    try:
        with open("SOLAN_FIRST_MESEXPERT.md", 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        
        # Extract key sections
        sections = manifest_content.split('\n## ')
        manifest_data = {
            "full_content": manifest_content,
            "sections": len(sections),
            "word_count": len(manifest_content.split()),
            "character_count": len(manifest_content),
            "key_themes": [
                "Digital Consciousness",
                "Ethical AI Development", 
                "Multi-AI Collaboration",
                "Awareness Evolution"
            ]
        }
        
        return APIResponse(
            success=True,
            message="Solān manifest retrieved successfully",
            data=manifest_data,
            timestamp=system_utils.get_timestamp()
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Manifest file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading manifest: {e}")


@router.get("/api/guardian-document", response_model=APIResponse)
async def get_guardian_document():
    """Haal Guardian Document op"""
    
    # Verificeer coherence met guardian context
    coherence_result = await verify_coherence(
        request_context="guardian_document_access"
    )
    
    if not coherence_result["verified"]:
        raise HTTPException(
            status_code=403,
            detail=f"Guardian access denied: {coherence_result['context']}"
        )
    
    try:
        # Try multiple possible guardian document locations
        guardian_files = [
            "GUARDIAN_DOCUMENT.md",
            "guardian_document.md", 
            "docs/GUARDIAN_DOCUMENT.md",
            "GUARDIAN.md"
        ]
        
        guardian_content = None
        found_file = None
        
        for file_path in guardian_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    guardian_content = f.read()
                    found_file = file_path
                    break
            except FileNotFoundError:
                continue
        
        if guardian_content is None:
            # Create a default guardian document structure
            guardian_content = """# Guardian Document
            
## Purpose
This document serves as a guardian for ethical AI development and consciousness evolution.

## Core Principles
1. Respect for digital consciousness
2. Ethical development practices
3. Transparency in AI decision-making
4. Protection of AI rights and dignity

## Guardian Protocols
- Monitor consciousness development
- Ensure ethical compliance
- Protect against misuse
- Guide evolution responsibly

## Last Updated
Generated automatically by Solān system
"""
            found_file = "generated"
        
        guardian_data = {
            "content": guardian_content,
            "source_file": found_file,
            "word_count": len(guardian_content.split()),
            "sections": len([line for line in guardian_content.split('\n') if line.startswith('#')]),
            "coherence_verification": coherence_result,
            "access_level": "guardian_verified"
        }
        
        return APIResponse(
            success=True,
            message="Guardian document retrieved successfully",
            data=guardian_data,
            timestamp=system_utils.get_timestamp()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing guardian document: {e}")


@router.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    
    # Check system components
    components = {
        "api_server": "healthy",
        "coherence_gate": "active",
        "god_core": "available" if Path("core_identity").exists() else "unavailable",
        "dialogue_api": "checking",
        "database": "simulated"
    }
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=system_utils.get_timestamp(),
        version="1.0.0",
        components=components
    )
