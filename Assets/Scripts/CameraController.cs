using UnityEngine;
// by abdullah
using UnityEngine.UI;

public class CameraController : MonoBehaviour
{
    public Camera cam;
    //added by abdullah
    public bool useWebcam = false; // toggle between scene capture and webcam
    public UnityEngine.UI.RawImage previewImage;

    private WebCamTexture webcamTexture;
    //

    private void Awake()
    {

        if (!useWebcam) // added by abdullah
        {
            if (cam == null)
            {
                cam = Camera.main;
            }

            if (cam == null)
            {
                Debug.LogError("CameraController: no Camera assigned and Camera.main is null");
            }
        }
    }

    private void Start()
    {
        if (useWebcam)
        {
            // Log all available webcams
            Debug.Log("Webcams found: " + WebCamTexture.devices.Length);
            for (int i = 0; i < WebCamTexture.devices.Length; i++)
            {
                Debug.Log($"Webcam {i}: {WebCamTexture.devices[i].name}");
            }

            // Start the first available webcam
            StartWebcam();
        }
    }

    public void StartWebcam()
    {
        if (WebCamTexture.devices.Length > 0)
        {
            webcamTexture = new WebCamTexture();
            webcamTexture.Play();

            if (previewImage != null)
            {
                previewImage.texture = webcamTexture;
                previewImage.material.mainTexture = webcamTexture;

            }
        }
        else
        {
            Debug.LogError("CameraController: No webcame found!");
        }
    }

    public Texture2D CapturePhoto()
    {
        if (cam == null)
        {
            Debug.LogError("CapturePhoto: cam is null");
            return null;
        }

        RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
        cam.targetTexture = rt;
        cam.Render();
        RenderTexture.active = rt;

        Texture2D photo = new Texture2D(rt.width, rt.height, TextureFormat.RGB24, false);
        photo.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
        photo.Apply();

        cam.targetTexture = null;
        RenderTexture.active = null;
        Destroy(rt);

        return photo;
    }

    // bottom lines all added by abdullah 
   
    public Texture2D CaptureWebcamPhoto()
    {
        if (webcamTexture == null || !webcamTexture.isPlaying)
        {
            Debug.LogError("CameraController: Webcam not running");
            return null;
        }

        Texture2D photo = new Texture2D(webcamTexture.width, webcamTexture.height);
        photo.SetPixels(webcamTexture.GetPixels());
        photo.Apply();
        return photo;
    }

    public void StopWebcam()
    {
        if (webcamTexture != null && webcamTexture.isPlaying)
        {
            webcamTexture.Stop();
        }
    }


}