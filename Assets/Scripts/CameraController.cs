using System.Collections;
using UnityEngine;
// by abdullah
using UnityEngine.UI;

public class CameraController : MonoBehaviour
{
    public Camera cam;
    //added by abdullah
    public bool useWebcam = false; // toggle between scene capture and webcam
    public UnityEngine.UI.RawImage previewImage;
    [Range(0.1f, 1f)] public float previewMaxScreenWidth = 0.92f;
    [Range(0.1f, 1f)] public float previewMaxScreenHeight = 0.62f;

    private WebCamTexture webcamTexture;
    private RectTransform previewRect;
    private int lastScreenWidth;
    private int lastScreenHeight;
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
        if (previewImage != null)
        {
            previewRect = previewImage.rectTransform;
        }

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

    private void Update()
    {
        if (!useWebcam || previewRect == null || webcamTexture == null)
            return;

        if (Screen.width != lastScreenWidth || Screen.height != lastScreenHeight)
        {
            ResizePreviewToWindow();
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
                StartCoroutine(ResizePreviewWhenReady());

            }
        }
        else
        {
            Debug.LogError("CameraController: No webcame found!");
        }
    }

    private IEnumerator ResizePreviewWhenReady()
    {
        while (webcamTexture != null && webcamTexture.width <= 16)
        {
            yield return null;
        }

        ResizePreviewToWindow();
    }

    private void ResizePreviewToWindow()
    {
        if (previewRect == null || webcamTexture == null)
            return;

        float textureWidth = Mathf.Max(webcamTexture.width, 1);
        float textureHeight = Mathf.Max(webcamTexture.height, 1);
        float aspect = textureWidth / textureHeight;

        float maxWidth = Screen.width * previewMaxScreenWidth;
        float maxHeight = Screen.height * previewMaxScreenHeight;

        float width = maxWidth;
        float height = width / aspect;

        if (height > maxHeight)
        {
            height = maxHeight;
            width = height * aspect;
        }

        previewRect.SetSizeWithCurrentAnchors(RectTransform.Axis.Horizontal, width);
        previewRect.SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical, height);

        lastScreenWidth = Screen.width;
        lastScreenHeight = Screen.height;
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
