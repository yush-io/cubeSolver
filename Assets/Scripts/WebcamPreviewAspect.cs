using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(RawImage))]
public sealed class WebcamPreviewAspect : MonoBehaviour
{
    [SerializeField] private Vector2 maxSize = Vector2.zero;

    private RawImage previewImage;
    private RectTransform previewRect;
    private int lastTextureWidth = -1;
    private int lastTextureHeight = -1;
    private int lastRotation = -1;

    private void Awake()
    {
        previewImage = GetComponent<RawImage>();
        previewRect = GetComponent<RectTransform>();

        if (maxSize == Vector2.zero)
        {
            maxSize = previewRect.sizeDelta;
        }
    }

    private void LateUpdate()
    {
        if (previewImage == null || previewImage.texture == null)
        {
            return;
        }

        Texture texture = previewImage.texture;
        int textureWidth = texture.width;
        int textureHeight = texture.height;

        // WebCamTexture reports placeholder dimensions for the first few frames.
        if (textureWidth <= 32 || textureHeight <= 32)
        {
            return;
        }

        int rotation = 0;
        if (texture is WebCamTexture webcamTexture)
        {
            rotation = webcamTexture.videoRotationAngle;
        }

        if (textureWidth == lastTextureWidth &&
            textureHeight == lastTextureHeight &&
            rotation == lastRotation)
        {
            return;
        }

        lastTextureWidth = textureWidth;
        lastTextureHeight = textureHeight;
        lastRotation = rotation;

        bool sideways = rotation == 90 || rotation == 270;
        float textureAspect = sideways
            ? textureHeight / (float)textureWidth
            : textureWidth / (float)textureHeight;

        Vector2 bounds = maxSize;
        if (bounds.x <= 0f || bounds.y <= 0f)
        {
            bounds = previewRect.rect.size;
        }

        if (bounds.x <= 0f || bounds.y <= 0f)
        {
            return;
        }

        float fittedWidth = bounds.x;
        float fittedHeight = fittedWidth / textureAspect;

        if (fittedHeight > bounds.y)
        {
            fittedHeight = bounds.y;
            fittedWidth = fittedHeight * textureAspect;
        }

        previewRect.SetSizeWithCurrentAnchors(RectTransform.Axis.Horizontal, fittedWidth);
        previewRect.SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical, fittedHeight);
    }
}
