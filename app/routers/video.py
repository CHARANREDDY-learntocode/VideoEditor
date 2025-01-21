from flask import Blueprint, request, jsonify, send_from_directory
from services.video_service import save_video, trim_video, merge_videos, generate_link
from models import Video, SharedLink, db
from datetime import datetime

video_bp = Blueprint('video', __name__)


@video_bp.route('/upload-video', methods=['POST'])
def upload_video():
    file = request.files['video']

    new_video, error = save_video(file)
    if error:
        return jsonify({"success": False, "message": error}), 400
    db.session.commit()
    return jsonify({"success": True, "message": "Video uploaded successfully.", "video_id": new_video.id}), 201


@video_bp.route('/trim-video/<filename>', methods=['POST'])
def trim_video_route(filename):
    start_time = float(request.json.get('start_time', 0))
    end_time = float(request.json.get('end_time', 0))

    trimmed_video, error = trim_video(filename, start_time, end_time)
    if error:
        return jsonify({"success": False, "message": error}), 400
    db.session.commit()
    return jsonify({"success": True, "message": "Video trimmed successfully.", "video_id": trimmed_video.id}), 200


@video_bp.route('/merge-videos', methods=['POST'])
def merge_videos_route():
    video_files = request.json.get('videos')  # List of filenames to merge

    merged_video, error = merge_videos(video_files)
    if error:
        return jsonify({"success": False, "message": error}), 400
    db.session.commit()
    return jsonify({"success": True, "message": "Videos merged successfully.", "video_id": merged_video.id}), 200


@video_bp.route('/generate-link/<int:video_id>', methods=['GET'])
def generate_link_route(video_id):
    expiry_time = int(request.args.get('expiry_time', 60))  # Expiry time in minutes, default 60 minutes

    shared_link, expiry_time = generate_link(video_id, expiry_time)
    if not shared_link:
        return jsonify({"success": False, "message": "Video not found."}), 404
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Link generated successfully.",
        "link": f"/video/shared/{video_id}/{shared_link.token}",
        "expires_at": expiry_time
    }), 200


@video_bp.route('/shared/<int:video_id>/<token>', methods=['GET'])
def shared_video_route(video_id, token):
    shared_link = SharedLink.query.filter_by(video_id=video_id, token=token).first()

    if not shared_link:
        return jsonify({"success": False, "message": "Link expired or invalid."}), 404

    if datetime.now() > shared_link.expiry_time:
        db.session.delete(shared_link)
        db.session.commit()
        return jsonify({"success": False, "message": "Link expired."}), 410

    video = Video.query.get(video_id)
    if not video:
        return jsonify({"success": False, "message": "Video not found."}), 404
    db.session.commit()
    return send_from_directory('uploads', video.filename)