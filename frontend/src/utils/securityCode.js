const SYMBOLS = ['@', '#', '$', '%', '&', '*', '!'];
const NUMBERS = ['2', '3', '4', '5', '6', '7', '8', '9'];
const UPPERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'R', 'T', 'W', 'X', 'Y', 'Z'];
const LOWERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n', 'p', 'r', 't', 'w', 'x', 'y', 'z'];

/**
 * Generates a 6-character code with 6 DIFFERENT characters,
 * strictly containing symbols, numbers, and alphabets.
 */
export const generateSixCharCode = () => {
  const selected = new Set();
  const pick = (arr) => {
    const valid = arr.filter((ch) => !selected.has(ch));
    const ch = valid[Math.floor(Math.random() * valid.length)];
    selected.add(ch);
    return ch;
  };
  pick(SYMBOLS);
  pick(NUMBERS);
  pick(UPPERS);
  pick(LOWERS);

  const pool = [...SYMBOLS, ...NUMBERS, ...UPPERS, ...LOWERS];
  while (selected.size < 6) pick(pool);

  const arr = Array.from(selected);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.join('');
};
