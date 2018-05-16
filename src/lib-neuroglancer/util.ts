
export const matchPythonURL = (key: string) => {
  const match = /^((https?:\/\/)?((.*)\/)*)(.*\/?)$/g.exec(key) || [];
  const baseURL = match[2] + match[4] || '';
  const hash = match[5] || '';
  return { baseURL, hash };
};
