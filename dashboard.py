from flask import Flask, render_template_string

app = Flask(__name__)

# This is the HTML code we designed, stored as a Python string
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utah Land & Property | Secure Asset Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,900&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --bhhs-cabernet: #631D33; --bhhs-gold: #85714D; --overlay: rgba(0, 0, 0, 0.55); }
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Montserrat', sans-serif; background-color: #fcfcfc; color: #1a1a1a; scroll-behavior: smooth; overflow-x: hidden; }
        .hero-container { position: relative; height: 100vh; width: 100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070'); background-size: cover; background-position: center; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; text-align: center; transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.6s ease; }
        .header-nav { position: absolute; top: 0; width: 100%; padding: 2.5rem 4rem; display: flex; justify-content: space-between; align-items: center; z-index: 50; }
        .logo-text { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.5rem; letter-spacing: 1px; line-height: 1.1; }
        .logo-subtext { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 3px; font-weight: 400; }
        .hero-title { font-family: 'Playfair Display', serif; font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 700; margin-bottom: 0.5rem; text-shadow: 2px 2px 15px rgba(0,0,0,0.5); }
        .hero-subtitle { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 6px; margin-bottom: 3rem; font-weight: 300; }
        .action-bar { background: white; padding: 0.5rem; display: flex; width: 90%; max-width: 900px; box-shadow: 0 15px 50px rgba(0,0,0,0.5); border-radius: 2px; }
        .action-input { flex-grow: 1; border: none; padding: 1.2rem 2rem; font-size: 1rem; color: #333; outline: none; }
        .action-button { background: var(--bhhs-cabernet); color: white; padding: 0 2.5rem; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: none; }
        #portal-overlay { position: fixed; inset: 0; background: rgba(99, 29, 51, 0.98); z-index: 100; display: none; flex-direction: column; align-items: center; justify-content: center; color: white; backdrop-filter: blur(12px); opacity: 0; transition: opacity 0.5s ease; }
        .portal-card { background: white; padding: 3.5rem; width: 100%; max-width: 480px; text-align: center; color: #333; }
        .btn-cabernet { background: var(--bhhs-cabernet); color: white; width: 100%; padding: 1.2rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 1.5rem; border: none; }
        #dashboard-view { display: none; opacity: 0; transition: opacity 1s ease-in-out; }
        .glass-card { background: white; border: 1px solid #e5e7eb; box-shadow: 0 4px 20px rgba(0,0,0,0.04); }
        .accent-border { border-left: 5px solid var(--bhhs-cabernet); }
        .visible { display: block !important; opacity: 1 !important; }
        .fade-out-up { transform: translateY(-100%); opacity: 0; }
    </style>
</head>
<body>
    <div style="height: 6px; background: var(--bhhs-cabernet); position: fixed; top:0; width: 100%; z-index: 1000;"></div>

    <section id="hero-section" class="hero-container">
        <header class="header-nav">
            <div class="flex flex-col text-left">
                <div class="logo-text uppercase">Utah Land & Property</div>
                <div class="logo-subtext">Luxury Asset Management</div>
            </div>
            <div class="hidden md:flex gap-10 text-[11px] uppercase tracking-[3px] font-medium items-center">
                <button onclick="togglePortal()" class="border border-white px-8 py-2 hover:bg-white hover:text-black transition">Secure Login</button>
            </div>
        </header>
        <div class="z-10 px-6">
            <h1 class="hero-title">Experience Elevated.</h1>
            <p class="hero-subtitle">The Gold Standard in Utah Real Estate Portfolio Management</p>
            <div class="action-bar mx-auto">
                <input type="text" id="main-search" class="action-input" placeholder="Enter Portfolio ID...">
                <button onclick="togglePortal()" class="action-button">Access Vault</button>
            </div>
        </div>
    </section>

    <section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
        <nav class="bg-white border-b border-gray-100 px-10 py-8 flex justify-between items-center sticky top-0 z-50">
            <div class="flex flex-col">
                <div class="text-[var(--bhhs-cabernet)] font-serif font-bold text-2xl tracking-tight uppercase">Private Client Portfolio</div>
                <div class="text-[10px] uppercase tracking-[4px] text-gray-400 mt-1" id="active-id-display">ID: NOT_LOADED</div>
            </div>
            <button onclick="location.reload()" class="text-gray-400 hover:text-[var(--bhhs-cabernet)] transition text-lg"><i class="fa-solid fa-circle-xmark"></i></button>
        </nav>
        <div class="max-w-7xl mx-auto px-10 mt-16">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-16">
                <div class="glass-card accent-border p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Projected Asset Value</div>
                    <div class="text-4xl font-serif font-bold text-[var(--bhhs-cabernet)]">$8,740,200</div>
                </div>
                <div class="glass-card p-10"><div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Land Utilization</div><div class="text-4xl font-serif font-bold">18.42 AC</div></div>
                <div class="glass-card p-10"><div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Market Liquidity</div><div class="text-4xl font-serif font-bold">Premium</div></div>
            </div>
        </div>
    </section>

    <div id="portal-overlay">
        <div class="portal-card shadow-2xl" id="portal-card">
            <div class="text-[var(--bhhs-cabernet)] font-serif text-3xl mb-3">Private Access Vault</div>
            <input type="password" id="token" class="w-full border-b border-gray-300 py-3 outline-none text-xl text-center mb-6" placeholder="••••••••">
            <button onclick="handleLogin()" class="btn-cabernet">Enter Secure Portal</button>
        </div>
    </div>

    <script>
        function togglePortal() {
            const overlay = document.getElementById('portal-overlay');
            overlay.style.display = 'flex';
            setTimeout(() => overlay.style.opacity = '1', 10);
            document.getElementById('token').value = document.getElementById('main-search').value;
        }
        function handleLogin() {
            document.getElementById('portal-overlay').style.display = 'none';
            document.getElementById('hero-section').classList.add('fade-out-up');
            setTimeout(() => {
                document.getElementById('hero-section').style.display = 'none';
                document.getElementById('dashboard-view').classList.add('visible');
                document.getElementById('active-id-display').innerText = 'ID: ' + document.getElementById('token').value.toUpperCase();
            }, 700);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML)

if __name__ == '__main__':
    # You will need to install flask first: pip install flask
    app.run(debug=True, port=5000)
"""
