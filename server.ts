import express from "express";
import path from "path";
import fs from "fs";
import { createServer as createViteServer } from "vite";
import { spawn } from "child_process";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API endpoint to compile and run code
  app.post("/api/run", (req, res) => {
    const { code, inputs, event } = req.body;
    
    // Spawn python3 with compiler.py
    const child = spawn("python3", ["compiler.py"]);
    
    let stdoutData = "";
    let stderrData = "";
    
    // Safety mechanism: terminate execution if it exceeds 4 seconds (e.g., infinite loops like "iken dogru")
    const timeout = setTimeout(() => {
      try {
        child.kill("SIGKILL");
      } catch (e) {
        // ignore error if process already exited
      }
      if (!res.writableEnded) {
        res.status(200).json({
          translated: "",
          ast: null,
          output: "",
          error: "Süre Aşımı: Kodunuzun çalışması 4 saniyeyi aştı. Sonsuz bir döngüye (örn: 'iken dogru') girmiş olabilir!"
        });
      }
    }, 4000);
    
    // Write request body to process stdin
    try {
      child.stdin.write(JSON.stringify({ code: code || "", inputs: inputs || [], event: event || null }));
      child.stdin.end();
    } catch (writeErr) {
      clearTimeout(timeout);
      if (!res.writableEnded) {
        res.status(200).json({
          translated: "",
          ast: null,
          output: "",
          error: `Veri iletilemedi: ${(writeErr as Error).message}`
        });
      }
      return;
    }
    
    child.stdout.on("data", (data) => {
      stdoutData += data.toString();
    });
    
    child.stderr.on("data", (data) => {
      stderrData += data.toString();
    });
    
    child.on("close", (exitCode) => {
      clearTimeout(timeout);
      
      if (res.writableEnded) return;
      
      // If there's an actual python standard error, return it
      if (stderrData.trim()) {
        res.status(200).json({
          translated: "",
          ast: null,
          output: "",
          error: `Sistem Çalışma Hatası (Python StdErr): ${stderrData}`
        });
        return;
      }
      
      try {
        const parsed = JSON.parse(stdoutData);
        res.json(parsed);
      } catch (err) {
        res.status(200).json({
          translated: "",
          ast: null,
          output: stdoutData || "",
          error: `Sonuç çözümlenirken hata oluştu: ${(err as Error).message}`
        });
      }
    });
  });

  // API endpoint to run automated unit tests on the core engine
  app.post("/api/tests/run", (req, res) => {
    const child = spawn("python3", ["tests/run_tests.py"]);
    let stdoutData = "";
    let stderrData = "";

    child.stdout.on("data", (data) => {
      stdoutData += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderrData += data.toString();
    });

    child.on("close", (code) => {
      res.json({
        success: code === 0,
        output: stdoutData + (stderrData ? "\n" + stderrData : "")
      });
    });
  });

  // API endpoint to list packages
  app.get("/api/packages", (req, res) => {
    try {
      const repoPath = path.join(process.cwd(), "ozdil", "repository.json");
      let registryPackages: any[] = [];
      if (fs.existsSync(repoPath)) {
        try {
          const repoData = JSON.parse(fs.readFileSync(repoPath, "utf-8"));
          registryPackages = repoData.paketler || [];
        } catch (e) {
          console.error("repository.json okuma hatası:", e);
        }
      }

      const packagesDir = path.join(process.cwd(), "oz_packages");
      const list = registryPackages.map((pkg: any) => {
        const isInstalled = fs.existsSync(path.join(packagesDir, pkg.isim));
        let installedVersion = "";
        if (isInstalled) {
          try {
            const metaPath = path.join(packagesDir, pkg.isim, "ozpaket.json");
            if (fs.existsSync(metaPath)) {
              const meta = JSON.parse(fs.readFileSync(metaPath, "utf-8"));
              installedVersion = meta.surum || pkg.surum;
            } else {
              installedVersion = pkg.surum;
            }
          } catch (e) {
            installedVersion = pkg.surum;
          }
        }
        return {
          ...pkg,
          installed: isInstalled,
          installedVersion
        };
      });
      res.json({ success: true, packages: list });
    } catch (err) {
      res.status(500).json({ success: false, error: (err as Error).message });
    }
  });

  // API endpoint to install a package
  app.post("/api/packages/install", (req, res) => {
    const { name } = req.body;
    if (!name) {
      res.status(400).json({ success: false, error: "Paket adı belirtilmelidir." });
      return;
    }

    // Safety validation on package name
    if (!/^[a-zA-Z0-9_]+$/.test(name)) {
      res.status(400).json({ success: false, error: "Geçersiz paket adı! Sadece harfler, sayılar ve alt çizgi kullanılabilir." });
      return;
    }

    const child = spawn("python3", ["ozpip.py", "install", name]);
    let stdoutData = "";
    let stderrData = "";

    child.stdout.on("data", (data) => {
      stdoutData += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderrData += data.toString();
    });

    child.on("close", (code) => {
      if (code !== 0 || stderrData.trim()) {
        res.json({
          success: false,
          output: stdoutData,
          error: stderrData || `Yükleme hatası (kod: ${code})`
        });
      } else {
        res.json({
          success: true,
          output: stdoutData
        });
      }
    });
  });

  // API endpoint to uninstall a package
  app.post("/api/packages/uninstall", (req, res) => {
    const { name } = req.body;
    if (!name) {
      res.status(400).json({ success: false, error: "Paket adı belirtilmelidir." });
      return;
    }

    // Safety validation on package name
    if (!/^[a-zA-Z0-9_]+$/.test(name)) {
      res.status(400).json({ success: false, error: "Geçersiz paket adı! Sadece harfler, sayılar ve alt çizgi kullanılabilir." });
      return;
    }

    const child = spawn("python3", ["ozpip.py", "uninstall", name]);
    let stdoutData = "";
    let stderrData = "";

    child.stdout.on("data", (data) => {
      stdoutData += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderrData += data.toString();
    });

    child.on("close", (code) => {
      if (code !== 0 || stderrData.trim()) {
        res.json({
          success: false,
          output: stdoutData,
          error: stderrData || `Kaldırma hatası (kod: ${code})`
        });
      } else {
        res.json({
          success: true,
          output: stdoutData
        });
      }
    });
  });

  // API endpoint to export code and runner files as a zip project
  app.post("/api/export", (req, res) => {
    const { code } = req.body;
    
    const child = spawn("python3", ["make_zip.py"]);
    
    let stdoutData = "";
    let stderrData = "";
    
    child.stdin.write(JSON.stringify({ code: code || "" }));
    child.stdin.end();
    
    child.stdout.on("data", (data) => {
      stdoutData += data.toString();
    });
    
    child.stderr.on("data", (data) => {
      stderrData += data.toString();
    });
    
    child.on("close", (exitCode) => {
      if (stderrData.trim()) {
        res.status(500).json({ error: `Sıkıştırma Hatası: ${stderrData}` });
        return;
      }
      
      try {
        const parsed = JSON.parse(stdoutData);
        if (parsed.success && parsed.filename) {
          const zipPath = path.join(process.cwd(), parsed.filename);
          
          if (fs.existsSync(zipPath)) {
            // Send file to client
            res.download(zipPath, "ozdil_projesi.zip", (err) => {
              // Delete zip file after download completed or failed
              try {
                fs.unlinkSync(zipPath);
              } catch (unlinkErr) {
                console.error("Temp zip silinemedi:", unlinkErr);
              }
            });
          } else {
            res.status(404).json({ error: "Oluşturulan zip dosyası bulunamadı." });
          }
        } else {
          res.status(500).json({ error: parsed.error || "Zip oluşturulamadı." });
        }
      } catch (err) {
        res.status(500).json({ error: `JSON çözme hatası: ${(err as Error).message}` });
      }
    });
  });

  // Serve Vite in development, static files in production
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
