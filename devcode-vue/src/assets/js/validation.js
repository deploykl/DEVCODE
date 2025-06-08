// utils.js
export function toLowerCase(value) {
  return value.toLowerCase();
}

export function limitInputLength(value, maxLength) {
  return value.length > maxLength ? value.slice(0, maxLength) : value;
}
