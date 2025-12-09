using UnityEngine;
using System.Collections.Generic;

public class CubeRotaterTestable : MonoBehaviour
{

        // fields
    public Transform upPivot;
    public Transform downPivot;
    public Transform leftPivot;
    public Transform rightPivot;
    public Transform frontPivot;
    public Transform backPivot;

      public Transform getPivot(string move)
    {

        if (string.IsNullOrEmpty(move))
        return null;

        char pivot = move[0];

        if (pivot == 'U') return upPivot;
        else if (pivot == 'D') return downPivot;
        else if (pivot == 'L') return leftPivot;
        else if (pivot == 'R') return rightPivot;
        else if (pivot == 'F') return frontPivot;
        else if (pivot == 'B') return backPivot;
        else return null;
    } 

    
    public Vector3 getAxis(string move)
    {
            if (string.IsNullOrEmpty(move))
            return Vector3.zero;
            char m = move[0];


        if (move[0] == 'U') return Vector3.up;
        else if (move[0] == 'D') return Vector3.down;
        else if (move[0] == 'L') return Vector3.left;
        else if (move[0] == 'R') return Vector3.right;
        else if (move[0] == 'F') return Vector3.forward;
        else if (move[0] == 'B') return Vector3.back;
        else return Vector3.zero;
    }
    
    public string getReverse(string move) 
    {
        char last = move[move.Length - 1];

        if (last == '2') return move;
        else if (last == '\'') return move.Remove(move.Length - 1);
        else return move + '\'';
    }

}
