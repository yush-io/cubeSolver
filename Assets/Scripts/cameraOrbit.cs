using Unity.VisualScripting;
using UnityEngine;

// code adapted from youtu.be/jt1bQX4sUoA?si=8oK2Zc6Y8EH7kAP7
public class CameraOrbit : MonoBehaviour
{
    [SerializeField] private Transform cube;
    [SerializeField] private float sensitivity = 5f;
    [SerializeField] private float maximumOrbit = 10f;
    [SerializeField] private float minimumOrbit = 6f;

    private float orbitRadius = 5f;
    private float mouseX = 0f;
    private float mouseY = 0f;
    private const int LeftClick = 0;

    private void Update()
    {
        if (Input.GetMouseButton(LeftClick))
        {
            transform.LookAt(cube);

            mouseX = Input.GetAxis("Mouse X");
            mouseY = Input.GetAxis("Mouse Y");

            transform.eulerAngles += new Vector3(-mouseY * sensitivity, mouseX * sensitivity, 0);
        }

        orbitRadius -= Input.mouseScrollDelta.y / sensitivity;
        orbitRadius = Mathf.Clamp(orbitRadius, minimumOrbit, maximumOrbit);

        transform.position = cube.position - transform.forward * orbitRadius;
    }
}