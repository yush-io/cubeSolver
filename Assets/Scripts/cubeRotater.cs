using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.TextCore;
using System.Timers;
using UnityEngine.InputSystem;
using RubikCube;
using System;
// using System.Diagnostics; // also namespace errors
// using System.Numerics; // not needed? causing namespace problems

// TODO (ranked by priority):
//   - write test cases for rotate function and dependencies
//     - number of moves, 
//   - add scramble function by reversing solution string
//   - clear up comments and refine coding conventions

public class cubeRotator : MonoBehaviour
{
    // may need to add second string member for scramble
    private class Moves
    {
        public string[] moves;
    }
    //C:\Users\celso\rubixCube\Assets\Scripts\cubeRotater.cs
    public Transform upPivot;
    public Transform downPivot;
    public Transform leftPivot;
    public Transform rightPivot;
    public Transform frontPivot;
    public Transform backPivot;

    private string[] moves; // will be given from backend/json file 
    private List<Transform> allCubelets = new List<Transform>();

    void readMoves()
    {
        string path = "FIX: CHANGE TO ACTUAL PATHNAME"; // should come from json

        if (File.Exists(path))
        {
            string movesStr = File.ReadAllText(path);
            Moves moveList = JsonUtility.FromJson<Moves>(movesStr);
            moves = moveList.moves;
        }
        else
        {
            Debug.LogError("No file found in readMoves function\n");
            // how to handle error? (quit, restart, modify, etc.)
        }
    }

    IEnumerator executeMoves()
    {
        for (int i = 0; i < moves.Length; ++i)
        {
            Debug.Log("Executing rotation: " + moves[i] + '\n');
            yield return rotateFace(moves[i]);
            yield return new WaitForSeconds(0.05f);
        }
    }

    Transform getPivot(string move)
    {
        char pivot = move[0];

        if (pivot == 'U') return upPivot;
        else if (pivot == 'D') return downPivot;
        else if (pivot == 'L') return leftPivot;
        else if (pivot == 'R') return rightPivot;
        else if (pivot == 'F') return frontPivot;
        else if (pivot == 'B') return backPivot;
        else
        {
            Debug.LogError("ERROR: invalid pivot/move in getPivot\n");
            return null;
        }
    }

    // use of math function adapted from official unity 6.2 documentation.
    // face math adapted from https://en.wikipedia.org/wiki/Cube under the
    // "constructions" heading
    // 
    List<Transform> getFace(string move)
    {
        List<Transform> faceCubelets = new List<Transform>();
        float separation = 0.2f;

        for (int i = 0; i < allCubelets.Count; ++i)
        {
            Transform cubelet = allCubelets[i];
            if (move[0] == 'U' && Mathf.Abs(cubelet.position.y - 1f) < separation) // top y layer
            {
                faceCubelets.Add(cubelet);
            }
            else if (move[0] == 'D' && Mathf.Abs(cubelet.position.y + 1f) < separation) // bottom y layer
            {
                faceCubelets.Add(cubelet);
            }
            else if (move[0] == 'L' && Mathf.Abs(cubelet.position.x + 1f) < separation) // leftmost layer
            {
                faceCubelets.Add(cubelet);
            }
            else if (move[0] == 'R' && Mathf.Abs(cubelet.position.x - 1f) < separation) // rightmost layer
            {
                faceCubelets.Add(cubelet);
            }
            else if (move[0] == 'F' && Mathf.Abs(cubelet.position.z - 1f) < separation) // front face
            {
                faceCubelets.Add(cubelet);
            }
            else if (move[0] == 'B' && Mathf.Abs(cubelet.position.z + 1f) < separation) // back face
            {
                faceCubelets.Add(cubelet);
            }
            // else
            // {
            //     Debug.Log("Cubelet: " + cubelet + " not included in face\n");
            // }
        }
        return faceCubelets;
    }

    // rotation logic adapted from Transform.Rotate (Unity Manual)
    IEnumerator rotateFace(string move)
    {
        Transform pivot = getPivot(move);

        if (pivot == null)
        {
            Debug.LogError("ERROR: invalid pivot (rotateFace function)");
            yield break; // quit
        }

        List<Transform> faceCubelets = getFace(move);

        for (int i = 0; i < faceCubelets.Count; ++i)
        {
            faceCubelets[i].SetParent(pivot);
        }

        float angle = 90f; // no special add-ons/notation
        if (move.Contains("'")) angle = -90f; // ' (prime) symbol
        else if (move.Contains("2")) angle = 180f; // turn twice (180 deg. turn)

        Vector3 axis = getAxis(move);
        if (axis == Vector3.zero)
        {
            Debug.LogError("ERROR: invalid axis in rotateFace\n");
            yield break;
        }

        float duration = 0.5f; // (of animation)
        float timeElapsed = 0f; // start
        float totalDegrees = 0f; // rotations so far
        // float rotSpeed = 400f;
        while (timeElapsed < duration)
        {
            // float increment = rotSpeed * Time.deltaTime;
            float increment = (angle / duration) * Time.deltaTime;

            // Rotate(Vector3 axis, float angle, Space relativeTo = Space.Self)
            pivot.Rotate(axis, increment, Space.Self);

            timeElapsed += Time.deltaTime;
            totalDegrees += increment;
            yield return null; // ensure pausing coroutine at end of frame
        }

        // correct any errors in rotation
        pivot.Rotate(axis, angle - totalDegrees, Space.Self);

        // restore cubes to parent after rotation
        for (int i = 0; i < faceCubelets.Count; ++i)
        {
            faceCubelets[i].SetParent(transform);
        }

    }

    Vector3 getAxis(string move)
    {
        if (move[0] == 'U') return Vector3.up;
        else if (move[0] == 'D') return Vector3.down;
        else if (move[0] == 'L') return Vector3.left;
        else if (move[0] == 'R') return Vector3.right;
        else if (move[0] == 'F') return Vector3.forward;
        else if (move[0] == 'B') return Vector3.back;
        else
        {
            Debug.LogError("ERROR: invalid axis in getAxis\n");
            return Vector3.zero;
        }
    }

    void Start()
    {
        // save only cubelets under parent (cube) and put into list
        for (int i = 0; i < transform.childCount; ++i)
        {
            Transform obj = transform.GetChild(i);
            if (!obj.name.Contains("Pivot")) // is cubelet
            {
                allCubelets.Add(obj);
            }
        }

        // readMoves();
        // FIXME: HARDCODED MOVES FOR TESTING
        moves = new string[] { "U2", "R2'", "F2", "D2", "L2", "B'", "U'", "R2", "F", "D'", "L'", "B2" };
        StartCoroutine(executeMoves());

        return;
    }
}