<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utah Land & Property</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,900&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --bhhs-cabernet: #631D33;
            --bhhs-gold: #85714D;
            --overlay: rgba(0, 0, 0, 0.3);
        }

        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: 'Montserrat', sans-serif;
            overflow-x: hidden;
        }

        /* Hero Background Section */
        .hero-container {
            position: relative;
            height: 100vh;
            width: 100%;
            background-image: linear-gradient(var(--overlay), var(--overlay)), 
                              url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070');
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }

        /* Navigation Header */
        .header-nav {
            position: absolute;
            top: 0;
            width: 100%;
            padding: 2rem 4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 50;
        }

        .logo-text {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            font-size: 1.5rem;
            letter-spacing: 1px;
            line-height: 1.1;
        }

        .logo-subtext {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 400;
        }

        /* Main Hero Text */
        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.5rem, 6vw, 5rem);
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        }

        .hero-subtitle {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 6px;
            margin-bottom: 3rem;
            font-weight: 300;
        }

        /* The BHHS Action Bar (Search Bar) */
        .action-bar {
            background: white;
            padding: 0.5rem;
            display: flex;
            width: 90%;
            max-width: 900px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border-radius: 2px;
        }

        .action-input {
            flex-grow: 1;
            border: none;
            padding: 1.2rem 2rem;
            font-size: 1rem;
            color: #333;
            outline: none;
        }

        .action-button {
            background: var(--bhhs-cabernet);
            color: white;
            padding: 0 2.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: background 0.3s;
            cursor: pointer;
            border: none;
        }

        .action-button:hover {
            background: #4a1526;
        }

        /* Client Portal Overlay */
        #portal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(99, 29, 51, 0.95);
            z-index: 100;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            backdrop-filter: blur(5px);
        }

        .portal-card {
            background: white;
            padding: 3rem;
            width: 100%;
            max-width: 450px;
            text-align: center;
            color: #333;
        }

        .btn-cabernet {
            background: var(--bhhs-cabernet);
            color: white;
            width: 100%;
            padding: 1rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
            margin-top: 1rem;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: var(--bhhs-cabernet); }

    </style>
</head>
<body>

    <!-- Top Accent Bar -->
    <div style="height: 6px; background: var(--bhhs-cabernet); position: fixed; top:0; width: 100%; z-index: 100;"></div>

    <header class="header-nav">
        <div class="flex flex-col">
            <div class="logo-text">UTAH LAND & PROPERTY</div>
            <div class="logo-subtext">Luxury Asset Management</div>
        </div>
        <div class="hidden md:flex gap-8 text-[11px] uppercase tracking-[3px] font-medium">
            <a href="#" class="hover:text-gray-300 transition">Portfolio</a>
            <a href="#" class="hover:text-gray-300 transition">Market Data</a>
            <a href="javascript:void(0)" onclick="togglePortal()" class="border-b border-white pb-1">Client Access</a>
        </div>
    </header>

    <main class="hero-container">
        <h1 class="hero-title">Experience Elevated.</h1>
        <p class="hero-subtitle">Utah's Premier Land & Estate Portfolio</p>

        <div class="action-bar">
            <input type="text" class="action-input" placeholder="Enter address, city, or zip code...">
            <button class="action-button">Search</button>
        </div>

        <div class="mt-12 flex gap-10 text-[10px] uppercase tracking-[4px] font-semibold">
            <div class="cursor-pointer hover:opacity-70">Residential</div>
            <div class="cursor-pointer hover:opacity-70">Commercial</div>
            <div class="cursor-pointer hover:opacity-70">Luxury Land</div>
        </div>
    </main>

    <!-- Secure Portal Modal -->
    <div id="portal-overlay">
        <div class="portal-card shadow-2xl">
            <div class="text-[var(--bhhs-cabernet)] font-serif text-3xl mb-2">Private Client Access</div>
            <p class="text-[10px] uppercase tracking-[2px] text-gray-500 mb-8">Asset Verification Required</p>
            
            <div class="text-left mb-4">
                <label class="text-[10px] uppercase tracking-[1px] font-bold text-gray-400">Access Token</label>
                <input type="password" id="token" class="w-full border-b border-gray-300 py-2 outline-none focus:border-[var(--bhhs-cabernet)] transition-all">
            </div>

            <button onclick="handleLogin()" class="btn-cabernet">Enter Secure Portal</button>
            <button onclick="togglePortal()" class="mt-4 text-[10px] uppercase tracking-[2px] text-gray-400 hover:text-black">Cancel</button>
        </div>
    </div>

    <script>
        function togglePortal() {
            const overlay = document.getElementById('portal-overlay');
            overlay.style.display = (overlay.style.display === 'flex') ? 'none' : 'flex';
        }

        function handleLogin() {
            const token = document.getElementById('token').value;
            if(token) {
                // In a real app, this would redirect or show the private dashboard
                document.querySelector('.hero-title').innerText = "Welcome, Client.";
                document.querySelector('.hero-subtitle').innerText = "4402 SOUTH WASATCH BLVD Portfolio";
                togglePortal();
            } else {
                alert("Valid access token required.");
            }
        }
    </script>
</body>
</html>
