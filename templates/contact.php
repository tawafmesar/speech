<?php 
ob_start();

include 'include/ini.php';
include 'include/connect.php';

// Process form submission
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve and trim input values
    $name    = trim($_POST['name']);
    $email   = trim($_POST['email']);
    $message = trim($_POST['message']);

    // Basic validation
    if (empty($name) || empty($email) || empty($message)) {
        $msg = '<div class="alert alert-danger">Please fill in all fields.</div>';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $msg = '<div class="alert alert-danger">Please enter a valid email address.</div>';
    } else {
        // Prepare and execute insert query
        try {
            $stmt = $con->prepare("INSERT INTO inquire (name, email, details) VALUES (:name, :email, :details)");
            $stmt->bindParam(':name', $name);
            $stmt->bindParam(':email', $email);
            $stmt->bindParam(':details', $message);
            $stmt->execute();
            
            $msg = '<div class="alert alert-success">Your message has been sent successfully.</div>';
        } catch (PDOException $e) {
            $msg = '<div class="alert alert-danger">Failed to send your message: ' . $e->getMessage() . '</div>';
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Us</title>
    <!-- Include your CSS files here (Bootstrap for example) -->
    <link rel="stylesheet" href="path/to/bootstrap.css">
    <link rel="stylesheet" href="path/to/your-styles.css">
</head>
<body>
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-body p-5 form-background">
                    <h2 class="text-center mb-4"><i class="fas fa-envelope"></i> Contact Us</h2>
                    
                    <!-- Display operation message if exists -->
                    <?php 
                    if (isset($msg)) {
                        echo $msg;
                    }
                    ?>
                    
                    <form action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>" method="POST">
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-user"></i> Name</label>
                            <input type="text" name="name" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-envelope"></i> Email</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label"><i class="fas fa-comment-dots"></i> Message</label>
                            <textarea name="message" class="form-control" rows="5" required></textarea>
                        </div>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-custom w-50">Send Message 📩</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<?php
include 'include/footer.php';
?>
<!-- Include your JS files here -->
<script src="path/to/bootstrap.js"></script>
</body>
</html>
