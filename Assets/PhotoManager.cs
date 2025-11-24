using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class PhotoManager : MonoBehaviour
{
    [Header("References")]
    public CameraController cameraController;
    public APIClient apiClient;
    public List<RawImage> photoSlots;  // Should have exactly 6 slots
    public TextMeshProUGUI statusText;

    private List<Texture2D> capturedPhotos = new List<Texture2D>();
    private const int maxPhotos = 6;

    public void TakePicture()
    {
        Debug.Log("TakePicture called");

        if (cameraController == null)
        {
            Debug.LogError("CameraController is not assigned!");
            if (statusText != null) statusText.text = "Error: Camera not assigned!";
            return;
        }

        if (capturedPhotos.Count >= maxPhotos)
        {
            Debug.Log("All 6 photos already taken.");
            if (statusText != null) statusText.text = "All 6 photos already taken.";
            return;
        }
         // changed and added 
        Texture2D photo;
        if (cameraController.useWebcam)
        {
            photo = cameraController.CaptureWebcamPhoto();
        }
        else
        {
            photo = cameraController.CapturePhoto();
        }
        if (photo == null)
        {
            Debug.LogError("Photo capture failed!");
            if (statusText != null) statusText.text = "Failed to capture photo!";
            return;
        }

        Debug.Log("Photo captured: " + photo.width + "x" + photo.height);
         //

        if (photo == null)
        {
            Debug.LogError("Failed to capture photo!");
            if (statusText != null) statusText.text = "Failed to capture photo!";
            return;
        }

        capturedPhotos.Add(photo);

        if (photoSlots.Count >= capturedPhotos.Count && photoSlots[capturedPhotos.Count - 1] != null)
        {
            photoSlots[capturedPhotos.Count - 1].texture = photo;
        }

        Debug.Log($"Photo {capturedPhotos.Count} captured");

        if (statusText != null)
            statusText.text = $"Photo {capturedPhotos.Count} taken!";
    }

    public void SubmitPhotos()
    {
        Debug.Log("SubmitPhotos called");

        if (apiClient == null)
        {
            Debug.LogError("APIClient is not assigned!");
            if (statusText != null) statusText.text = "Error: APIClient not assigned!";
            return;
        }

        if (capturedPhotos.Count < maxPhotos)
        {
            Debug.Log("You must take all 6 photos before submitting.");
            if (statusText != null) statusText.text = $"Take all {maxPhotos} photos first!";
            return;
        }

        StartCoroutine(UploadPhotos());
    }

    private IEnumerator UploadPhotos()
    {
        if (statusText != null) statusText.text = "Uploading photos...";
        Debug.Log("Uploading photos...");

        yield return StartCoroutine(apiClient.SendPhotos(capturedPhotos));

        Debug.Log("Upload complete!");
        if (statusText != null) statusText.text = "Upload complete!";

        // If you want to change scene after upload, uncomment:
        // UnityEngine.SceneManagement.SceneManager.LoadScene("CubeSolverScene");
    }
}