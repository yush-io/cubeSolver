using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
//using UnityEngine.TextCore;
//using System.Timers;
//using UnityEngine.InputSystem;
//using RubikCube;
//using System;
//using System.Drawing;
// using System.Diagnostics; // also namespace errors
// using System.Numerics; // causing namespace problems


public class CubeRotator : MonoBehaviour
{
    // may need to add second string member for scramble
    private class Moves
    {
        public string[] moves;
    }

    // fields
    public Transform upPivot;
    public Transform downPivot;
    public Transform leftPivot;
    public Transform rightPivot;
    public Transform frontPivot;
    public Transform backPivot;


    bool inRotation = false;
    int moveIndex = -1; // start before first move

    private string[] moves; // will be given from backend/json file 
    private List<Transform> allCubelets = new List<Transform>();

    // constants
    const float normalTurn = 90f;
    const float twoTurns = 180f;
    const float primeTurn = -90f;

    // functions
    void readMoves()
    {
        string path = "FIX: CHANGE TO ACTUAL JSON PATHNAME";

        if (File.Exists(path))
        {
            string movesStr = File.ReadAllText(path);
            Moves moveList = JsonUtility.FromJson<Moves>(movesStr);
            moves = moveList.moves;
        }
        else
        {
            Debug.LogError("No file found in readMoves function\n");
        }
    }

    IEnumerator executeMoves(string[] moveList)
    {
        for (int i = 0; i < moveList.Length; ++i)
        {
            // Debug.Log("Executing rotation: " + moves[i] + '\n');
            yield return rotateFace(moveList[i]);
            yield return new WaitForSeconds(0.05f);
        }
    }

    public Transform getPivot(string move)
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

        float angle = normalTurn; 
        if (move.Contains("'")) angle = primeTurn; 
        else if (move.Contains("2")) angle = twoTurns; 

        Vector3 axis = getAxis(move);
        if (axis == Vector3.zero)
        {
            Debug.LogError("ERROR: invalid axis in rotateFace\n");
            yield break;
        }

        float animationDuration = 0.5f;
        float timeElapsed = 0f;
        float totalDegreesRotated = 0f;
        while (timeElapsed < animationDuration)
        {
            float increment = (angle / animationDuration) * Time.deltaTime;

            pivot.Rotate(axis, increment, Space.Self);

            timeElapsed += Time.deltaTime;
            totalDegreesRotated += increment;
            yield return null; // ensure pausing coroutine at end of frame
        }

        // correct any errors in rotation
        pivot.Rotate(axis, angle - totalDegreesRotated, Space.Self);

        // restore cubes to parent after rotation
        for (int i = 0; i < faceCubelets.Count; ++i)
        {
            faceCubelets[i].SetParent(transform);
        }

    }

    public Vector3 getAxis(string move)
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

    public string getReverse(string move) 
    {
        char last = move[move.Length - 1];

        if (last == '2') return move;
        else if (last == '\'') return move.Remove(move.Length - 1);
        else return move + '\'';
    }

    // button funcitonality partially adapted from 
    // https://www.youtube.com/watch?v=gSfdCke3684
    IEnumerator executeMove(string move)
    {
        inRotation = true;
        yield return rotateFace(move);
        inRotation = false;
    }

    public void nextMove()
    {
        if (inRotation) return; // no button spam
        if (moveIndex == moves.Length - 1) return;
        
        ++moveIndex;
        StartCoroutine(executeMove(moves[moveIndex]));
    }

    public void previousMove()
    {
        if (inRotation) return;
        if (moveIndex < 0) return;

        string reverse = getReverse(moves[moveIndex]);
        StartCoroutine(executeMove(reverse));
        --moveIndex;
    }

    void Start()
    {
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
        string[] scramble = new string[] { "U2", "R2", "F2", "D2", "L2", "B'", "U'", "R2", "F", "D'", "L'", "B2" };
        StartCoroutine(executeMoves(scramble));

        moves = new string[scramble.Length];

        for (int i = 0; i < scramble.Length; ++i)
        {
            string move = scramble[scramble.Length - 1 - i];
            moves[i] = getReverse(move);
        }

        return;
    }
}