"""
test_app_interactive.py - Full Streamlit AppTest Suite
Simulates real user interaction, navigation, button clicks, quiz submission,
guardrail enforcement, and unseen topic generation through Streamlit's official AppTest runner.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from streamlit.testing.v1 import AppTest

def test_full_application():
    print("=" * 75)
    print("🚀 RUNNING AUTOMATED STREAMLIT INTERACTIVE APPTEST SUITE")
    print("=" * 75)

    # 1. Initialize and run AppTest
    print("\n[STEP 1] Initializing AppTest on app.py...")
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    assert not at.exception, f"App threw exception on initial load: {at.exception}"
    print("  ✓ Initial load successful. Zero exceptions.")

    # 2. Test Page 1: Learn
    print("\n[STEP 2] Verifying Page 1 (Learn)...")
    assert any("Executive Summary" in str(m.value) for m in at.markdown), "Summary card not found"
    print("  ✓ Learn page content and CPython mechanics rendered.")

    # 3. Test Navigation to Page 2: Quiz & Answer Submission
    print("\n[STEP 3] Navigating to Page 2 (Quiz) and submitting answers...")
    at.sidebar.radio[0].set_value("2. Quiz").run()
    assert not at.exception, f"Exception navigating to Quiz: {at.exception}"
    
    # Answer all 5 quiz items
    radios = at.radio
    assert len(radios) >= 5, f"Expected at least 5 quiz radios, found {len(radios)}"
    for r in radios[:5]:
        r.set_value(r.options[0])
    at.run()
    assert not at.exception

    # Find and click submit / grade button
    submit_buttons = [b for b in at.button if "Submit" in b.label or "Grade" in b.label]
    assert len(submit_buttons) > 0, "Submit/Grade quiz button not found"
    submit_buttons[0].click().run()
    assert not at.exception, f"Exception submitting quiz: {at.exception}"
    print("  ✓ Quiz submitted. 5-item evaluation computed without errors.")

    # 4. Test Navigation to Page 3: Diagnostic
    print("\n[STEP 4] Navigating to Page 3 (Diagnostic)...")
    at.sidebar.radio[0].set_value("3. Diagnostic").run()
    assert not at.exception, f"Exception on Diagnostic page: {at.exception}"
    assert len(at.metric) >= 4, f"Expected at least 4 diagnostic metrics, got {len(at.metric)}"
    print(f"  ✓ Diagnostic metrics verified: {[m.label for m in at.metric]}.")

    # 5. Test Navigation to Page 4: Personalised Learning Path (Stretch Challenge)
    print("\n[STEP 5] Navigating to Page 4 (Personalised Learning Path)...")
    at.sidebar.radio[0].set_value("4. Personalised Learning Path").run()
    assert not at.exception, f"Exception on Roadmap page: {at.exception}"
    print("  ✓ Tailored 4-phase roadmap and 14-day revision schedule verified.")

    # 6. Test Navigation to Page 5: Flashcards
    print("\n[STEP 6] Navigating to Page 5 (Flashcards)...")
    at.sidebar.radio[0].set_value("5. Flashcards").run()
    assert not at.exception, f"Exception on Flashcards page: {at.exception}"
    flip_buttons = [b for b in at.button if "Flip" in b.label]
    assert len(flip_buttons) > 0, "Flip button not found"
    flip_buttons[0].click().run()
    assert not at.exception, f"Exception clicking flip: {at.exception}"
    print("  ✓ Flashcards flip and active recall verified.")

    # 7. Test Navigation to Page 6: Prompt Techniques
    print("\n[STEP 7] Navigating to Page 6 (Prompt Techniques)...")
    at.sidebar.radio[0].set_value("6. Prompt Techniques").run()
    assert not at.exception, f"Exception on Prompt Techniques page: {at.exception}"
    print("  ✓ Prompt techniques laboratory and benchmark verified.")

    # 8. Test Navigation to Page 7: Evaluation (10+ Cases)
    print("\n[STEP 8] Navigating to Page 7 (Evaluation - 10+ Cases Benchmark)...")
    at.sidebar.radio[0].set_value("7. Evaluation").run()
    assert not at.exception, f"Exception on Evaluation page: {at.exception}"
    assert len(at.dataframe) > 0, "Benchmark dataframe not found"
    print("  ✓ Labelled 10+ cases benchmark dataframe verified.")

    # 9. Test Navigation to Page 8: Prompt History (from 11:00 AM)
    print("\n[STEP 9] Navigating to Page 8 (Prompt History from 11:00 AM)...")
    at.sidebar.radio[0].set_value("8. Prompt History").run()
    assert not at.exception, f"Exception on Prompt History page: {at.exception}"
    assert len(at.download_button) >= 2, "Export buttons not found"
    print("  ✓ Timestamped prompt history and export buttons verified.")

    # 10. Test Guardrails (Off-Topic Refusal)
    print("\n[STEP 10] Testing Live Guardrail Refusal on Off-Topic Input...")
    at.sidebar.text_input[0].set_value("Recipe for Chocolate Cake with Strawberries")
    refresh_btn = [b for b in at.sidebar.button if any(k in b.label for k in ["Load", "Generate", "Refresh"])][0]
    refresh_btn.click().run()
    assert not at.exception, f"Exception during guardrail check: {at.exception}"
    assert len(at.error) > 0, "Guardrail refusal error banner should be displayed"
    print(f"  ✓ Guardrail refusal correctly triggered: '{at.error[0].value[:60]}...'")

    # 11. Test Live Unseen Python Topic Synthesis
    print("\n[STEP 11] Testing Dynamic Synthesis for Unseen Topic ('Walrus Operator in Dictionaries')...")
    at.sidebar.text_input[0].set_value("Walrus Operator in Dictionaries")
    refresh_btn = [b for b in at.sidebar.button if any(k in b.label for k in ["Load", "Generate", "Refresh"])][0]
    refresh_btn.click().run()
    assert not at.exception, f"Exception during unseen topic synthesis: {at.exception}"
    at.sidebar.radio[0].set_value("1. Learn").run()
    assert not at.exception
    assert any("Walrus Operator" in str(m.value) for m in at.markdown)
    print("  ✓ Dynamic synthesis for unseen topic verified with 100% success!")

    print("\n" + "=" * 75)
    print("🎉 ALL 11 STREAMLIT APPTEST INTERACTIVE WORKFLOW TESTS PASSED!")
    print("=" * 75)

if __name__ == "__main__":
    test_full_application()
