/**
 * Formats a number or string as a currency string without decimals and with thousand separators.
 * Example: 5400.00 -> 5,400
 */
export function formatCurrency(value) {
  const num = typeof value === 'number' ? value : parseFloat(value || 0);
  if (isNaN(num)) return '0';
  
  return Math.round(num).toLocaleString('en-US');
}
