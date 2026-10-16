// Current published demo: focused smoke with optional HTTP Basic auth.
// Original Gemini-reviewed v1 suite: qa-browser-v1.cjs (synthetic-upload legacy).
// Full current workflows: qa-workspaces.cjs + qa-workspaces-extra.cjs on staging.
if(process.argv.includes('--legacy'))require('./qa-browser-v1.cjs');
else require('./qa-private-smoke.cjs');
