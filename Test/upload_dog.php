<?php
// Проверяем, была ли отправлена форма
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Получаем данные о собаке
    $dogName = $_POST['dogName'];
    $dogAge = $_POST['dogAge'];
    $dogBreed = $_POST['dogBreed'];
    $dogCharacter = $_POST['dogCharacter'];

    // Получаем информацию о файле изображения
    $fileName = $_FILES['dogImage']['name'];
    $fileTmpName = $_FILES['dogImage']['tmp_name'];
    $fileSize = $_FILES['dogImage']['size'];
    $fileError = $_FILES['dogImage']['error'];

    // Проверяем, что файл был загружен без ошибок
    if ($fileError === 0) {
        // Перемещаем файл из временной директории в папку uploads с уникальным именем
        $fileDestination = 'uploads/' . $fileName;
        move_uploaded_file($fileTmpName, $fileDestination);

        // TODO: Сохраняем информацию о собаке в базу данных или другое хранилище

        // Возвращаемся на страницу с формой с сообщением об успешном добавлении
        header("Location: add_dog.html?uploadsuccess");
    } else {
        // Если произошла ошибка при загрузке файла, выводим сообщение об ошибке
        echo "Произошла ошибка при загрузке файла.";
    }
}
?>
