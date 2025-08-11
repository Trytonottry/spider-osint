import asyncio
import argparse
from core.engine import SpiderEngine
from db.database import init_db

def main():
    parser = argparse.ArgumentParser(description="🕷️ SPIDER — OSINT Framework with AI")
    parser.add_argument("--target", required=True, help="Target: email, phone, domain, etc.")
    parser.add_argument("--modules", nargs="+", default=["all"], help="Modules to run")
    parser.add_argument("--report", action="store_true", help="Generate PDF/HTML report")
    parser.add_argument("--ask", help="Ask AI assistant")
    args = parser.parse_args()

    init_db()
    engine = SpiderEngine(target=args.target, modules=args.modules, args=args)
    results = asyncio.run(engine.run())

    if args.report:
        engine.generate_report(results)

    if args.ask:
        from ai.assistant import OSINTAssistant
        assistant = OSINTAssistant()
        answer = assistant.ask(args.ask, str(results))
        print(f"[AI] {answer}")

    print("[+] OSINT completed.")

if __name__ == "__main__":
    main()