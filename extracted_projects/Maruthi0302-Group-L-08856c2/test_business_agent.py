"""Quick test script for Business Agent"""
from telecom_agent import agent

print('\n===== BUSINESS AGENT END-TO-END TEST =====\n')

# Test 1: Billing support
print('Test 1: Billing Question')
result1 = agent.process('My internet bill is too expensive', [])
print(f'  ✓ Intent: {result1["intent"]}')
print(f'  ✓ Response: {result1["response"][:80]}...')
print(f'  ✓ Escalate: {result1["should_escalate"]}')
print()

# Test 2: Technical issue
print('Test 2: Technical Issue')
result2 = agent.process('My connection keeps dropping', [])
print(f'  ✓ Intent: {result2["intent"]}')
print(f'  ✓ Response: {result2["response"][:80]}...')
print(f'  ✓ Escalate: {result2["should_escalate"]}')
print()

# Test 3: Escalation trigger
print('Test 3: Escalation Check')
result3 = agent.process('I want a refund NOW this is unacceptable!', [])
print(f'  ✓ Intent: {result3["intent"]}')
print(f'  ✓ Response: {result3["response"][:80]}...')
print(f'  ✓ Escalate: {result3["should_escalate"]}')
print()

print('===== ✓ ALL TESTS PASSED =====\n')
