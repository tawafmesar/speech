<?php
// audio-sample.php
// This template displays audio files from various folders using Bootstrap nav tabs.
// Adjust the paths as needed if your directory structure differs.

// Function to fetch audio files (.wav) from a specific folder.
function getAudioFiles($folder) {
    // Assuming the 'sample' folder is one directory above 'templates'
    $path = realpath(__DIR__ . '/../sample/' . $folder);
    if (!$path) {
        return [];
    }
    // Get all .wav files
    return glob($path . "/*.wav");
}

// Retrieve files for each emotion
$angryFiles    = getAudioFiles("angry");
$disgustFiles  = getAudioFiles("disgust");
$fearFiles     = getAudioFiles("fear");
$happyFiles    = getAudioFiles("happy");
$neutralFiles  = getAudioFiles("neutral");
$sadFiles      = getAudioFiles("sad");
$surpriseFiles = getAudioFiles("surprise");

// Merge all files for the "All Audio" tab and randomize the order.
$allFiles = array_merge($angryFiles, $disgustFiles, $fearFiles, $happyFiles, $neutralFiles, $sadFiles, $surpriseFiles);
shuffle($allFiles);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Audio Sample Gallery</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <style>
    body {
      background: #f8f9fa;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
      margin-bottom: 30px;
    }
    .audio-container {
      padding-top: 20px;
    }
    .audio-item {
      background: #ffffff;
      border-radius: 5px;
      padding: 15px;
      margin-bottom: 15px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .audio-item p {
      margin-bottom: 10px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container my-5">
    <h1 class="text-center">Audio Samples</h1>
    <!-- Nav Tabs -->
    <ul class="nav nav-tabs" id="audioTab" role="tablist">
      <li class="nav-item">
        <a class="nav-link active" id="all-tab" data-toggle="tab" href="#all" role="tab">All Audio</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="angry-tab" data-toggle="tab" href="#angry" role="tab">Angry</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="disgust-tab" data-toggle="tab" href="#disgust" role="tab">Disgust</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="fear-tab" data-toggle="tab" href="#fear" role="tab">Fear</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="happy-tab" data-toggle="tab" href="#happy" role="tab">Happy</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="neutral-tab" data-toggle="tab" href="#neutral" role="tab">Neutral</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="sad-tab" data-toggle="tab" href="#sad" role="tab">Sad</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="surprise-tab" data-toggle="tab" href="#surprise" role="tab">Surprise</a>
      </li>
    </ul>
    <!-- Tab Content -->
    <div class="tab-content" id="audioTabContent">
      <!-- All Audio Tab -->
      <div class="tab-pane fade show active" id="all" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($allFiles)): ?>
            <?php foreach ($allFiles as $file): 
              // Determine relative path: get parent folder name & file name.
              $folderName = basename(dirname($file));
              $fileName   = basename($file);
              $relativePath = "../sample/$folderName/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Angry Tab -->
      <div class="tab-pane fade" id="angry" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($angryFiles)): ?>
            <?php foreach ($angryFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/angry/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Angry folder.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Disgust Tab -->
      <div class="tab-pane fade" id="disgust" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($disgustFiles)): ?>
            <?php foreach ($disgustFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/disgust/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Disgust folder.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Fear Tab -->
      <div class="tab-pane fade" id="fear" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($fearFiles)): ?>
            <?php foreach ($fearFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/fear/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Fear folder.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Happy Tab -->
      <div class="tab-pane fade" id="happy" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($happyFiles)): ?>
            <?php foreach ($happyFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/happy/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Happy folder.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Neutral Tab -->
      <div class="tab-pane fade" id="neutral" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($neutralFiles)): ?>
            <?php foreach ($neutralFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/neutral/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Neutral folder.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Sad Tab -->
      <div class="tab-pane fade" id="sad" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($sadFiles)): ?>
            <?php foreach ($sadFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/sad/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Sad folder.</p>
          <?php endif; ?>
        </div>
      </div>
      <!-- Surprise Tab -->
      <div class="tab-pane fade" id="surprise" role="tabpanel">
        <div class="audio-container">
          <?php if (!empty($surpriseFiles)): ?>
            <?php foreach ($surpriseFiles as $file): 
              $fileName = basename($file);
              $relativePath = "../sample/surprise/$fileName";
            ?>
              <div class="audio-item">
                <p><?php echo htmlspecialchars($fileName); ?></p>
                <audio controls>
                  <source src="<?php echo $relativePath; ?>" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
              </div>
            <?php endforeach; ?>
          <?php else: ?>
            <p>No audio files found in the Surprise folder.</p>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </div>

  <!-- Bootstrap JS and dependencies -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
