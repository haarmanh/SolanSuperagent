#!/bin/bash

# Solān v3.0 Production Verification Script
# Usage: ./verify-production.sh

echo "🔍 SOLĀN v3.0 PRODUCTION VERIFICATION"
echo "===================================="

API_BASE="https://api.solanai.ai"
HEALTH_ENDPOINT="$API_BASE/api/health"
BIAS_ENDPOINT="$API_BASE/api/analyzer/bias"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_TOTAL=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    echo -n "Testing $test_name... "
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    result=$(eval "$test_command" 2>/dev/null)
    exit_code=$?
    
    if [ $exit_code -eq 0 ] && [[ $result =~ $expected_pattern ]]; then
        echo -e "${GREEN}✅ PASSED${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        echo "   Expected: $expected_pattern"
        echo "   Got: $result"
        return 1
    fi
}

echo ""
echo "🌐 DNS & Connectivity Tests"
echo "----------------------------"

# Test 1: DNS Resolution
run_test "DNS Resolution" "nslookup api.solanai.ai | grep -E 'Address: [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'" "Address:"

# Test 2: HTTPS Connectivity
run_test "HTTPS Connectivity" "curl -s -o /dev/null -w '%{http_code}' $HEALTH_ENDPOINT" "200"

# Test 3: Health Endpoint
run_test "Health Endpoint" "curl -s $HEALTH_ENDPOINT" '"status":"ok"'

echo ""
echo "🔒 Security Tests"
echo "-----------------"

# Test 4: TLS Certificate
run_test "TLS Certificate" "curl -s -I $HEALTH_ENDPOINT | grep -i 'HTTP/2 200'" "HTTP/2 200"

# Test 5: Security Headers
run_test "Security Headers" "curl -s -I $HEALTH_ENDPOINT | grep -i 'x-frame-options'" "X-Frame-Options"

echo ""
echo "🧪 Functionality Tests"
echo "----------------------"

# Test 6: Bias Detection
run_test "Bias Detection" "curl -s -X POST -H 'Content-Type: application/json' -d '{\"text\":\"Women are always more emotional\"}' $BIAS_ENDPOINT" '"findings"'

# Test 7: PII Redaction
pii_test_result=$(curl -s -X POST -H 'Content-Type: application/json' -d '{"text":"Contact me at test@example.com or call 123-456-7890"}' $BIAS_ENDPOINT)
if [[ $pii_test_result == *"test@example.com"* ]] || [[ $pii_test_result == *"123-456-7890"* ]]; then
    echo -e "Testing PII Redaction... ${RED}❌ FAILED${NC}"
    echo "   PII found in response: $pii_test_result"
else
    echo -e "Testing PII Redaction... ${GREEN}✅ PASSED${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi
TESTS_TOTAL=$((TESTS_TOTAL + 1))

echo ""
echo "⏱️ Rate Limiting Test"
echo "---------------------"

echo "Testing rate limiting (this may take a moment)..."
rate_limit_triggered=false
for i in {1..65}; do
    http_code=$(curl -s -o /dev/null -w '%{http_code}' $HEALTH_ENDPOINT)
    if [ "$http_code" = "429" ]; then
        echo -e "Rate Limiting... ${GREEN}✅ PASSED${NC} (triggered at request $i)"
        rate_limit_triggered=true
        TESTS_PASSED=$((TESTS_PASSED + 1))
        break
    fi
    sleep 0.1
done

if [ "$rate_limit_triggered" = false ]; then
    echo -e "Rate Limiting... ${YELLOW}⚠️ WARNING${NC} (not triggered after 65 requests)"
fi
TESTS_TOTAL=$((TESTS_TOTAL + 1))

echo ""
echo "📊 VERIFICATION SUMMARY"
echo "======================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}/$TESTS_TOTAL"

if [ $TESTS_PASSED -eq $TESTS_TOTAL ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! Solān v3.0 is fully operational!${NC}"
    echo ""
    echo "🌟 Your API endpoints:"
    echo "   Health:    $HEALTH_ENDPOINT"
    echo "   Bias:      $API_BASE/api/analyzer/bias"
    echo "   Alignment: $API_BASE/api/analyzer/alignment"
    echo "   Coherence: $API_BASE/api/analyzer/coherence"
    echo "   Logs:      $API_BASE/api/logs/tail"
    echo ""
    echo "🔗 Ready to integrate with your frontend!"
    exit 0
else
    echo -e "${RED}⚠️ Some tests failed. Please check the issues above.${NC}"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   - Check DNS propagation: nslookup api.solanai.ai"
    echo "   - Verify containers: docker-compose ps"
    echo "   - Check logs: docker-compose logs -f"
    exit 1
fi
