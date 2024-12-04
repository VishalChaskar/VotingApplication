import psycopg2
from flask import Flask, render_template, request, jsonify
from flask import Flask, jsonify
import cv2
from deepface import DeepFace

app = Flask(__name__)

# Mock data
candidates = ["Mit", "Vishal", "Prathamesh"]
votes = {candidate: 0 for candidate in candidates}


@app.route("/")
def index():
    return render_template("index.html", candidates=candidates, votes=votes)


@app.route("/vote", methods=["POST"])
def vote():
    voter_id = request.form.get("voter_id")
    candidate = request.form.get("candidate")

    # For simplicity, we skip voter ID validation
    if candidate in votes:
        votes[candidate] += 1
        return jsonify({"success": True, "message": f"Vote cast for {candidate}!"})
    return jsonify({"success": False, "message": "Invalid candidate!"})


@app.route('/capture-image', methods=['POST'])
def capture_image():
    try:
        img1_path = "Vishal1.jpg"
        img2_path = "webcam_image.png"

        # Start the webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({"message": "Error: Could not open webcam."}), 500

        print("Press 'Enter' to capture an image.")

        # Configure the OpenCV window
        window_name = "Webcam - Press 'Enter' to capture"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture webcam frame.")
                break

            # Display the webcam feed
            cv2.imshow(window_name, frame)

            # Wait for the 'Enter' key press
            key = cv2.waitKey(1)
            if key == 13:  # Enter key

                cv2.imwrite(img2_path, frame)
                print("Image captured.")
                break

        # Release the webcam and close OpenCV window
        cap.release()
        cv2.destroyAllWindows()

        # Perform face verification
        try:
            result = DeepFace.verify(img1_path, img2_path, enforce_detection=False).get('verified')
            print("Verification result:", result)
            jsonify({"message": "Verification complete.", "result": result})
            return result
        except Exception as e:
            jsonify({"message": f"DeepFace verification failed: {str(e)}"}), 500
            return result

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)


def deb_con():
    conn = psycopg2.connect(database="VOTERS", host="localhost", user="postgres", password="admin", port="5432")
    return conn
