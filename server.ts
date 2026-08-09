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
    const { code } = req.body;
    
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
      child.stdin.write(JSON.stringify({ code: code || "" }));
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
