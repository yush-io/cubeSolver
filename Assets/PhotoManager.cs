using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;

public class PhotoManager : MonoBehaviour
{
    [Header("References")]
    public CameraController cameraController;
    public APIClient apiClient;
    public List<RawImage> photoSlots;  // Should have exactly 6 slots
    public TextMeshProUGUI statusText;
    private readonly string[] scanPrompts =
    {
        "Capture the face with the WHITE center",
        "Capture the face with the RED center",
        "Capture the face with the GREEN center",
        "Capture the face with the YELLOW center",
        "Capture the face with the ORANGE center",
        "Capture the face with the BLUE center"
    };

    private List<Texture2D> capturedPhotos = new List<Texture2D>();
    private const int maxPhotos = 6;

    private void Start()
    {
        UpdateScanPrompt();
    }
    private void UpdateScanPrompt()
    {
        if (statusText == null) return;

        if (capturedPhotos.Count < maxPhotos)
        {
            statusText.text = scanPrompts[capturedPhotos.Count];
        }
        else
        {
            statusText.text = "All 6 faces captured. Submit photos.";
        }
    }
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

        capturedPhotos.Add(photo);

        if (photoSlots.Count >= capturedPhotos.Count && photoSlots[capturedPhotos.Count - 1] != null)
        {
            photoSlots[capturedPhotos.Count - 1].texture = photo;
        }

        Debug.Log($"Photo {capturedPhotos.Count} captured");

        UpdateScanPrompt();
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
            UpdateScanPrompt();
            return;
        }

        StartCoroutine(UploadPhotos());
    }

    private IEnumerator UploadPhotos()
    {
        if (statusText != null) statusText.text = "Uploading photos...";
        Debug.Log("Uploading photos...");

        
        yield return StartCoroutine(apiClient.SendPhotos(capturedPhotos, OnSolutionReceived));

        Debug.Log("Upload complete!");
    }

    private void OnSolutionReceived(string[] solution)
    {
        // initial checks
        if(solution == null || solution.Length == 0)
        {
            Debug.LogError("No solution returned!");
            if (statusText != null) 
                statusText.text = "No solution returned!";
            return;
        }
        Debug.Log("Solution from backend: " + string.Join(" ", solution));

        SolutionStore.LatestSolution = solution;
        Debug.Log("PhotoManager: Stored solution in SolutionStore. Length = " + solution.Length);

        // now loads not on button click but after solution is stored. 
        // wont move on if no solution in SolutionStore static class 
        SceneManager.LoadScene("SampleScene");
    }

}