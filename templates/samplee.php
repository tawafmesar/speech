<?php
include 'include/ini.php';
include 'include/connect.php';

// Function to get audio files from database
function getAudioFilesFromDB($emotion = null) {
  global $con; 
    
    $query = "SELECT a.file_name, e.name AS emotion 
              FROM audio_files a
              JOIN emotions e ON a.emotion_id = e.emotion_id";
              
    if ($emotion) {
        $query .= " WHERE e.name = :emotion";
        $stmt = $con->prepare($query);
        $stmt->execute(['emotion' => $emotion]);
    } else {
        $stmt = $con->query($query);
    }
    
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Get all emotions for tabs
$stmt = $con->query("SELECT name FROM emotions");
$emotions = $stmt->fetchAll(PDO::FETCH_COLUMN);

// Get all files for "All Audio" tab
$allFiles = getAudioFilesFromDB();
shuffle($allFiles);
?>

<!-- Keep the same HTML structure but modify the PHP parts -->
<style>
    body {
        background: #f8f9fa;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        margin-bottom: 30px;
        font-weight: bold;
        color: #333;
    }
    .audio-container {
        padding-top: 20px;
    }
    .audio-item {
        background: #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
    }
    .audio-item:hover {
        transform: scale(1.02);
    }
    .audio-item p {
        margin-bottom: 10px;
        font-weight: bold;
    }
    /* تحسين شكل عناصر الـ nav */
    .nav-tabs {
        border-bottom: 2px solid #007bff;
    }

   .nav-tabs .nav-link {
        color: #333;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        padding: 10px 15px;
    }
   .nav-tabs .nav-link:hover {
        background: #007bff;
        color: #fff;
        box-shadow: 0 2px 5px rgba(0, 123, 255, 0.4);
    }
    .nav-tabs .nav-link.active {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: #fff !important;
        font-weight: bold;
        box-shadow: 0 3px 6px rgba(0, 123, 255, 0.4);
    }
</style>

<div class="container my-5">
    <h1 class="text-center">Audio Samples</h1>
    <ul class="nav nav-tabs" id="audioTab" role="tablist">
        <?php foreach ($emotions as $index => $emotion): ?>
            <li class="nav-item">
                <a class="nav-link <?= $index === 0 ? 'active' : '' ?>" 
                   id="<?= $emotion ?>-tab" 
                   data-toggle="tab" 
                   href="#<?= $emotion ?>" 
                   role="tab">
                   <?= ucfirst($emotion) ?> <?= getEmoji($emotion) ?>
                </a>
            </li>
        <?php endforeach; ?>
    </ul>

    <div class="tab-content" id="audioTabContent">
        <?php foreach ($emotions as $index => $emotion): ?>
            <div class="tab-pane fade <?= $index === 0 ? 'show active' : '' ?>" 
                 id="<?= $emotion ?>" 
                 role="tabpanel">
                <div class="audio-container">
                    <?php $files = getAudioFilesFromDB($emotion); ?>
                    <?php if (!empty($files)): ?>
                        <?php foreach ($files as $file): ?>
                            <div class="audio-item">
                                <p><?= htmlspecialchars($file['file_name']) ?></p>
                                <audio controls>
                                    <source src="../sample/<?= $file['emotion'] ?>/<?= $file['file_name'] ?>" 
                                            type="audio/wav">
                                    Your browser does not support the audio element.
                                </audio>
                            </div>
                        <?php endforeach; ?>
                    <?php else: ?>
                        <p>No audio files found for <?= ucfirst($emotion) ?></p>
                    <?php endif; ?>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>
  <!-- Bootstrap JS and dependencies -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
<?php
// Helper function for emojis
function getEmoji($emotion) {
    $emojis = [
        'angry' => '😠',
        'disgust' => '🤢',
        'fear' => '😨',
        'happy' => '😊',
        'neutral' => '😐',
        'sad' => '😢',
        'surprise' => '😲'
    ];
    return $emojis[$emotion] ?? '';
}
include 'include/footer.php';
?>