import unittest
import os
from werkzeug.datastructures import FileStorage
from datetime import datetime
from models import Video, SharedLink, db
from services.video_service import save_video, merge_videos, trim_video, generate_link


class VideoServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        cls.upload_folder = 'test_mock_data'
        if not os.path.exists(cls.upload_folder):
            os.makedirs(cls.upload_folder)

    def setUp(self):
        """Initialize the Flask app and database for each test."""
        from main import app
        self.app = app
        self.client = self.app.test_client()

        # Configure the app for testing
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder

        # Create the database tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after tests."""
        # Delete files in the test upload folder
        for file in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Drop the database tables
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_save_video(self):
        """Test saving a video to the database."""
        with self.app.app_context():
            with open("mock_data/video1.mp4", "rb") as file:
                file_storage = FileStorage(
                    stream=file,
                    filename="video1.mp4",
                    content_type="video/mp4"
                )
                video, error = save_video(file_storage)

            self.assertIsNone(error)
            self.assertIsNotNone(video)
            self.assertEqual(video.filename, "video1.mp4")

            saved_video = Video.query.filter_by(filename="video1.mp4").first()
            self.assertIsNotNone(saved_video)
            self.assertEqual(saved_video.filename, "video1.mp4")

    def test_merge_videos(self):
        """Test merging videos."""
        with self.app.app_context():
            with open("mock_data/video1.mp4", "rb") as file1, open("mock_data/video2.mp4", "rb") as file2:
                # Save the videos
                video1, _ = save_video(FileStorage(stream=file1, filename="video1.mp4", content_type="video/mp4"))
                video2, _ = save_video(FileStorage(stream=file2, filename="video2.mp4", content_type="video/mp4"))

            # Merge the videos
            merged_video, error = merge_videos([video1.filename, video2.filename])

            self.assertIsNone(error)
            self.assertIsNotNone(merged_video)
            self.assertTrue(merged_video.filename.startswith("merged_"))

    def test_trim_video(self):
        """Test trimming a video."""
        with self.app.app_context():
            with open("mock_data/video1.mp4", "rb") as file:
                # Save the video
                video, _ = save_video(FileStorage(stream=file, filename="video1.mp4", content_type="video/mp4"))

            # Trim the video
            trimmed_video, error = trim_video(video.filename, start_time=5, end_time=10)

            self.assertIsNone(error)
            self.assertIsNotNone(trimmed_video)
            self.assertTrue(trimmed_video.filename.startswith("trimmed_"))

    def test_generate_shared_link(self):
        """Test generating a shared link for a video."""
        with self.app.app_context():
            # Save the video
            with open("mock_data/video1.mp4", "rb") as file:
                file_storage = FileStorage(
                    stream=file,
                    filename="video1.mp4",
                    content_type="video/mp4"
                )
                video, error = save_video(file_storage)
                self.assertIsNone(error)
                self.assertIsNotNone(video)

            # Verify video exists
            saved_video = Video.query.filter_by(filename="video1.mp4").first()
            self.assertIsNotNone(saved_video)

            # Generate a shared link
            expiry_minutes = 60
            shared_link, expiry_time = generate_link(saved_video.id, expiry_time_minutes=expiry_minutes)

            # Debug: Print shared link details
            print(f"Shared Link: {shared_link}, Expiry Time: {expiry_time}")

            self.assertIsNotNone(shared_link)
            self.assertIsNotNone(expiry_time)
            self.assertEqual(shared_link.video_id, saved_video.id)
            self.assertTrue(isinstance(shared_link.token, str))
            self.assertTrue((expiry_time - datetime.now()).seconds <= expiry_minutes * 60)

            # Verify shared link exists in the database
            saved_link = SharedLink.query.filter_by(token=shared_link.token).first()
            self.assertIsNotNone(saved_link)
            self.assertEqual(saved_link.video_id, saved_video.id)

if __name__ == '__main__':
    unittest.main()