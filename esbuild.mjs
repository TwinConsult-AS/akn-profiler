import * as esbuild from "esbuild";

const production = process.argv.includes("--production");
const watch = process.argv.includes("--watch");

/** @type {import('esbuild').BuildOptions} */
const buildOptions = {
    entryPoints: ["client/src/extension.ts"],
    bundle: true,
    format: "cjs",
    minify: production,
    sourcemap: !production,
    sourcesContent: false,
    platform: "node",
    outfile: "client/out/extension.js",
    external: ["vscode"],
    logLevel: "info",
    // Node built-ins used by vscode-languageclient
    mainFields: ["module", "main"],
};

async function main() {
    if (watch) {
        const ctx = await esbuild.context(buildOptions);
        await ctx.watch();
        console.log("[esbuild] watching for changes...");
    } else {
        await esbuild.build(buildOptions);
    }
}

main().catch((e) => {
    console.error(e);
    process.exit(1);
});
