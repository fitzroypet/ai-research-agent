import argparse
from datetime import datetime
import os
from langchain_community.chat_models import ChatOpenAI
from general_research import run_research
from youtube_research import run_youtube_research

def main():
    parser = argparse.ArgumentParser(description='AI Research Assistant')
    parser.add_argument('--type', choices=['general', 'youtube'], required=True,
                      help='Type of research to perform')
    parser.add_argument('--prompt', required=True,
                      help='Research prompt or niche description')
    parser.add_argument('--model', choices=['gpt-3.5-turbo', 'gpt-4-turbo-preview'],
                      default='gpt-3.5-turbo', help='OpenAI model to use')
    parser.add_argument('--temperature', type=float, default=0.7,
                      help='Model temperature (0.0-1.0)')
    args = parser.parse_args()

    # Configure OpenAI
    openai = ChatOpenAI(
        model=args.model,
        temperature=args.temperature
    )

    # Show configuration
    print("\n=== Configuration ===")
    print(f"Research Type: {args.type}")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Prompt: {args.prompt}")

    # Confirm configuration
    confirm = input("\nProceed with this configuration? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    # Run appropriate research
    if args.type == 'general':
        result = run_research(args.prompt)
    else:
        result = run_youtube_research(args.prompt)

    # Handle results
    if result:
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/{args.type}_research_{timestamp}.txt"
        
        # Preview and confirm save
        print("\n=== Results Preview ===")
        print(result[:500] + "...")
        save = input("\nSave results? (y/n): ")
        
        if save.lower() == 'y':
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"\nResults saved to: {output_file}")
        else:
            print("\nResults discarded.")

if __name__ == "__main__":
    main() 