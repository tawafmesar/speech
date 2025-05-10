<?php
// login.php
include 'include/ini.php';
include 'include/connect.php';


// If user is already logged in, redirect based on role
if (isset($_SESSION['accountType'])) {
  $role = strtolower($_SESSION['accountType']);

  if ($role === 'admin') {
      header("Location: admin.php");
      exit();
  } elseif ($role === 'user') {
      header("Location: index.php");
      exit();
  }
}


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve and sanitize form inputs
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    if (empty($username) || empty($password)) {
        $error = "Please fill in both username and password.";
    } else {
        try {
            // Prepare query to fetch user details from account table
            $stmt = $con->prepare("SELECT accountNo, accountType, username, password FROM account WHERE username = ?");
            $stmt->execute([$username]);
            $user = $stmt->fetch(PDO::FETCH_ASSOC);

            // Verify the password using password_verify() against the hashed password stored in the database
            if ($user && password_verify($password, $user['password'])) {
                // Set session variables
                $_SESSION['accountNo']   = $user['accountNo'];
                $_SESSION['username']    = $user['username'];
                $_SESSION['accountType'] = $user['accountType'];

              // Redirect based on role (case-insensitive)
              $role = strtolower($user['accountType']);

               if ($role === 'admin') {
                  header("Location: admin.php");
                  exit();
              } elseif ($role === 'user') {
                  header("Location: index.php");
                  exit();
              } else {
                  header("Location: index.php");
                  exit();
              }

            } else {
                $error = "Invalid credentials! Please try again.";
            }
        } catch (PDOException $e) {
            $error = "An error occurred: " . $e->getMessage();
        }
    }
}
?>

<body>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body p-5 form-background">
            <h2 class="text-center mb-4"><i class="fas fa-sign-in-alt"></i> Login</h2>
            <?php if(isset($error)): ?>
              <div class="alert alert-danger"><?php echo $error; ?></div>
            <?php endif; ?>
            <form id="loginForm" method="post" action="">
              <div class="mb-3">
                <label class="form-label"><i class="fas fa-user"></i> Username</label>
                <input type="text" name="username" id="usernameInput" class="form-control" required placeholder="Enter your username" />
              </div>
              <div class="mb-3">
                <label class="form-label"><i class="fas fa-lock"></i> Password</label>
                <input type="password" name="password" class="form-control" required placeholder="Enter your password" />
              </div>
              <button type="submit" class="btn btn-custom w-100">Login 🔑</button>
              <p class="text-center mt-3">
                Don't have an account? <a href="register.php">Register here 📝</a>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
<?php
include 'include/footer.php';
?>
