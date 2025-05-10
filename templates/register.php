<?php

// include necessary initialization and database connection files
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
// Process form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve and trim form inputs
    $fullName = trim($_POST['fullName']);
    $username = trim($_POST['username']);
    $email    = trim($_POST['email']);
    $phone    = trim($_POST['phone']);
    $password = trim($_POST['password']);

    // Basic validation: check that none of the fields are empty.
    if (empty($fullName) || empty($username) || empty($email) || empty($phone) || empty($password)) {
        $error = "Please fill in all required fields.";
    } else {
        try {
            // Begin transaction
            $con->beginTransaction();

            // Insert into account table (assume accountType "user" for registrants)
            $stmt = $con->prepare("INSERT INTO account (accountType, username, password) VALUES (?, ?, ?)");
            // Hash the password for security
            $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
            $stmt->execute(['user', $username, $hashedPassword]);

            // Retrieve the auto-generated account number
            $accountNo = $con->lastInsertId();

            // Insert into user table
            // Here, "name" is the full name and "users_name" is the username.
            $stmt2 = $con->prepare("INSERT INTO user (accountNo, phone, name, users_name, email) VALUES (?, ?, ?, ?, ?)");
            $stmt2->execute([$accountNo, $phone, $fullName, $username, $email]);

            // Commit the transaction
            $con->commit();

            $success = "Registration successful!";
        } catch (PDOException $e) {
            // Rollback if any error occurs
            $con->rollBack();
            $error = "Registration failed: " . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
    <!-- Add your CSS and other head elements here -->
</head>
<body>
<!-- Registration Page -->
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-5 form-background">
                    <h2 class="text-center mb-4"><i class="fas fa-user-plus"></i> Register</h2>
                    <?php if(isset($error)): ?>
                        <div class="alert alert-danger"><?php echo $error; ?></div>
                    <?php endif; ?>
                    <?php if(isset($success)): ?>
                        <div class="alert alert-success"><?php echo $success; ?></div>
                    <?php endif; ?>
                    <form action="" method="post">
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-user"></i> Full Name</label>
                            <input type="text" name="fullName" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-user"></i> Username</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-envelope"></i> Email</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-phone"></i> Phone</label>
                            <input type="text" name="phone" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-lock"></i> Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <div class="text-center">
                            <button type="submit" class="btn btn-custom w-50">Register 📝</button>
                        </div>
                        <p class="text-center mt-3">
                            Already have an account? <a href="login.php">Login here 🔑</a>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
<?php include 'include/footer.php'; ?>
</body>
</html>
