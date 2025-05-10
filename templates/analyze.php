<?php  
// login.php
include 'include/header.php';

$isAuthorized = false;
if (isset($_SESSION['accountType'])) {
    $role = strtolower($_SESSION['accountType']);
    $isAuthorized = ($role === 'admin' || $role === 'user');
}
?>

<?php if ($isAuthorized): ?>
    <div style="height: 100vh; width: 100%; overflow: hidden;">
    <iframe src="http://127.0.0.1:5000" allow="microphone" style="border: none; width: 100%; height: 100%;"></iframe>
        </div>
<?php else: ?>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes float {
            0% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0); }
        }

        .access-message {
            text-align: center;
            padding: 50px 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .message-box {
            animation: fadeIn 1s ease-in, float 2s ease-in-out 1s infinite;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .emoji {
            font-size: 4rem;
            margin-bottom: 20px;
        }
        
        .message-text {
            font-size: 1.5rem;
            color: #2c3e50;
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .btn-access {
            padding: 15px 40px;
            font-size: 1.2rem;
            border-radius: 30px;
            transition: all 0.3s ease;
            background: #4CAF50;
            color: white;
            border: none;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-access:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(76,175,80,0.3);
        }
    </style>

    <div class="access-message">
        <div class="message-box">
            <div class="emoji">🔒😊</div>
            <h1 class="message-text">
                Welcome to Speech Analysis!<br>
                <small style="font-size: 1rem; display: block; margin-top: 15px;">
                    Please login or register to unlock this awesome feature!
                </small>
            </h1>
            <div class="d-flex justify-content-center gap-3">
                <a href="login.php" class="btn btn-lg btn-primary px-5">
                    <i class="fas fa-sign-in-alt mr-2"></i>Login
                </a>
                <a href="register.php" class="btn btn-lg btn-success px-5">
                    <i class="fas fa-user-plus mr-2"></i>Register
                </a>
            </div>
        </div>
    </div>
<?php endif; ?>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

<?php include 'include/footer.php'; ?>