import Head from 'next/head';

export default function Observatorium() {
  return (
    <>
      <Head>
        <title>Solān Observatorium - SolanSuperagent</title>
        <meta name="description" content="Live Analyzer voor Bias, Alignment, Coherence en Audit Trail" />
      </Head>
      
      <main style={{
        padding: "2rem", 
        maxWidth: "1400px", 
        margin: "0 auto",
        minHeight: "100vh",
        backgroundColor: "#fafafa"
      }}>
        <div style={{
          marginBottom: "2rem",
          textAlign: "center"
        }}>
          <h1 style={{
            fontSize: "2.5rem",
            fontWeight: "bold",
            marginBottom: "0.5rem",
            color: "#1f2937"
          }}>
            Solān Observatorium
          </h1>
          <p style={{
            color: "#6b7280",
            fontSize: "1.1rem"
          }}>
            Live Analyzer • Bias Detection • Alignment • Coherence • Audit Trail
          </p>
        </div>
        
        <div style={{
          backgroundColor: "white",
          borderRadius: "16px",
          boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
          overflow: "hidden",
          border: "1px solid #e5e7eb"
        }}>
          <iframe
            src="/observatorium/index.html"
            title="Solān Observatorium"
            style={{
              width: "100%", 
              height: "85vh", 
              border: "none",
              display: "block"
            }}
          />
        </div>
        
        <div style={{
          marginTop: "1rem",
          textAlign: "center",
          color: "#9ca3af",
          fontSize: "0.875rem"
        }}>
          <a 
            href="/" 
            style={{
              color: "#3b82f6",
              textDecoration: "none",
              marginRight: "1rem"
            }}
          >
            ← Terug naar Dashboard
          </a>
          <span>|</span>
          <a 
            href="/observatorium/index.html" 
            target="_blank"
            style={{
              color: "#3b82f6",
              textDecoration: "none",
              marginLeft: "1rem"
            }}
          >
            Open in nieuw venster ↗
          </a>
        </div>
      </main>
    </>
  );
}
