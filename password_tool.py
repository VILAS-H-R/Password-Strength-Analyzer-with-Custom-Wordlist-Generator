import argparse
from zxcvbn import zxcvbn
import itertools

leet_dict = {'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['$', '5'], 't': ['7']}

def analyze_password(password):
    result = zxcvbn(password)
    print(f"\nPassword: {password}")
    print(f"Score: {result['score']} / 4")
    print("Feedback:", result['feedback']['warning'] or "Looks good.")
    print("Suggestions:", ', '.join(result['feedback']['suggestions']) or "None")

def leetify(word):
    substitutions = [[c] + leet_dict.get(c.lower(), []) for c in word]
    variants = set(''.join(combo) for combo in itertools.product(*substitutions))
    return list(variants)

def generate_wordlist(inputs):
    base_words = [word.lower() for word in inputs]
    variants = set()

    for word in base_words:
        variants.update([
            word,
            word.capitalize(),
            word[::-1],
            f"{word}123",
            f"{word}!",
        ])
        variants.update(leetify(word))
        for year in range(1990, 2031):
            variants.add(f"{word}{year}")

    return sorted(variants)

def export_wordlist(words, filename):
    with open(filename, 'w') as f:
        for word in words:
            f.write(f"{word}\n")
    print(f"Wordlist exported to {filename} with {len(words)} entries.")

def main():
    parser = argparse.ArgumentParser(description="Password Analyzer & Wordlist Generator")
    parser.add_argument('--analyze', help="Password to analyze")
    parser.add_argument('--inputs', nargs='+', help="Personal info (name, pet, etc.)")
    parser.add_argument('--outfile', default="custom_wordlist.txt", help="Output file name")

    args = parser.parse_args()

    if args.analyze:
        analyze_password(args.analyze)

    if args.inputs:
        words = generate_wordlist(args.inputs)
        export_wordlist(words, args.outfile)

if __name__ == "__main__":
    main()
