import subprocess
import sys

# Automatically handle installation of missing dependencies
def install_requirements():
    try:
        from flask import Flask, render_template_string
    except ImportError:
        print("Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("Flask installed successfully.")

# Run installation check before main logic
install_requirements()

from flask import Flask, render_template_string

app = Flask(__name__)

# Dashboard UI Content
# Using a raw string (r""") to prevent backslash escaping issues
DASHBOARD_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utah Land & Property | Secure Asset Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --bhhs-cabernet: #631D33; --bhhs-gold: #85714D; }
        body { font-family: 'Montserrat', sans-serif; background-color: #fcfcfc; }
        .hero-bg { 
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
            url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070');
            background-size: cover; background-position: center;
        }
        .font-serif-custom { font-family: 'Playfair Display', serif; }
        .secure-input { border-bottom: 2px solid var(--bhhs-cabernet) !important; }
    </style>
</head>
<body class="overflow-x-hidden">
    <!-- Header/Hero -->
    <div id="hero" class="hero-bg h-screen flex flex-col justify-center items-center text-white text-center transition-all duration-700">
        <div class="absolute top-10 left-10 flex flex-col items-start">
            <span class="font-serif-custom text-2xl tracking-widest">UTAH LAND & PROPERTY</span>
            <span class="text-[10px] tracking-[4px] opacity-70">PRIVATE ASSET MANAGEMENT</span>
        </div>
        
        <h1 class="font-serif-custom text-6xl mb-4">The Gold Standard.</h1>
        <p class="tracking-[6px] uppercase text-sm mb-12 opacity-90">Secure Portfolio Access</p>
        
        <div class="bg-white p-2 flex w-full max-w-lg shadow-2xl">
            <input type="text" id="auth-code" placeholder="Enter Portfolio Access ID" class="flex-1 p-4 text-black outline-none">
            <button onclick="unlock()" class="bg-[#631D33] px-8 py-4 font-bold tracking-widest text-xs uppercase hover:bg-black transition">Access</button>
        </div>
    </div>

    <!-- Hidden Dashboard -->
    <div id="dashboard" class="hidden opacity-0 transition-opacity duration-1000 min-h-screen bg-white">
        <nav class="p-8 border-b flex justify-between items-center bg-white sticky top-0 z-50">
            <div>
                <h2 class="font-serif-custom text-xl text-[#631D33]">CLIENT PORTFOLIO</h2>
                <p id="client-id" class="text-[9px] tracking-[3px] text-gray-400 uppercase font-bold"></p>
            </div>
            <button onclick="location.reload()" class="text-gray-300 hover:text-black transition text-xl"><i class="fa-solid fa-power-off"></i></button>
        </nav>

        <main class="max-w-7xl mx-auto p-10">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                <div class="p-8 border-l-4 border-[#631D33] shadow-sm bg-gray-50">
                    <p class="text-[10px] tracking-widest text-gray-400 uppercase mb-2">Portfolio Valuation</p>
                    <h3 class="text-3xl font-serif-custom">$12,450,000</h3>
                </div>
                <div class="p-8 border shadow-sm bg-white">
                    <p class="text-[10px] tracking-widest text-gray-400 uppercase mb-2">Total Acreage</p>
                    <h3 class="text-3xl font-serif-custom">42.85 AC</h3>
                </div>
                <div class="p-8 border shadow-sm bg-white">
                    <p class="text-[10px] tracking-widest text-gray-400 uppercase mb-2">Portfolio Status</p>
                    <h3 class="text-3xl font-serif-custom">Active</h3>
                </div>
            </div>

            <div class="bg-white border p-12 text-center">
                <i class="fa-solid fa-lock text-4xl text-gray-200 mb-4"></i>
                <h4 class="font-serif-custom text-2xl mb-2">Property Documentation</h4>
                <p class="text-gray-500 max-w-md mx-auto text-sm">Detailed legal descriptions, tax assessments, and topographical maps are being synced for this ID.</p>
            </div>
        </main>
    </div>

    <script>
        function unlock() {
            const code = document.getElementById('auth-code').value;
            if(!code) return;
            
            document.getElementById('hero').classList.add('-translate-y-full');
            setTimeout(() => {
                document.getElementById('hero').style.display = 'none';
                const dash = document.getElementById('dashboard');
                dash.classList.remove('hidden');
                document.getElementById('client-id').innerText = "Account ID: " + code.toUpperCase();
                setTimeout(() => dash.classList.add('opacity-100'), 50);
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
    # Using 0.0.0.0 ensures accessibility if deployed in a container/VM
    app.run(host='0.0.0.0', port=5000, debug=True)
