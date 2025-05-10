<?php  
session_start();

// Determine the current page name without the file extension
$currentPage = basename($_SERVER['PHP_SELF'], ".php");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speech Emotion Recognition</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="./css/style.css">
    <style>
        /* Add custom styles for active nav links */
        .navbar .nav-link.active {
            color: white !important;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <!-- Header -->
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="index.php">
                <img src="img/logo.png" alt="Assisted Living System" height="60">
            </a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <!-- Common Navigation Items -->
                    <li class="nav-item">
                        <a class="nav-link <?php echo ($currentPage == 'index') ? 'active' : ''; ?>" href="index.php">Home 🏠</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?php echo ($currentPage == 'analyze') ? 'active' : ''; ?>" href="analyze.php">Analyze 🧐</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?php echo ($currentPage == 'sample') ? 'active' : ''; ?>" href="sample.php">Sample 😌</a>
                    </li>
                   <li class="nav-item">
                        <a class="nav-link <?php echo ($currentPage == 'faq') ? 'active' : ''; ?>" href="faq.php">FAQ ❓</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?php echo ($currentPage == 'contact') ? 'active' : ''; ?>" href="contact.php">Contact Us 📞</a>
                    </li>

                    <?php if (isset($_SESSION['accountType'])): ?>
                        <!-- Dashboard links can be added here if needed -->
                        <li class="nav-item">
                            <a class="nav-link <?php echo ($currentPage == 'logout') ? 'active' : ''; ?>" href="logout.php">Logout 🚪</a>
                        </li>
                    <?php else: ?>
                        <li class="nav-item">
                            <a class="nav-link <?php echo ($currentPage == 'login') ? 'active' : ''; ?>" href="login.php">Login 🔑</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link <?php echo ($currentPage == 'register') ? 'active' : ''; ?>" href="register.php">Register 📝</a>
                        </li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>
    </nav>
    <!-- Rest of your page content -->
