using UnityEngine;

public class CharacterMotionController : MonoBehaviour
{
    private Animator animator;
    private Transform leftLowerArm;

    private Quaternion originalLeftArmRotation;

    void Start()
    {
        animator = GetComponent<Animator>();

        leftLowerArm = animator.GetBoneTransform(
            HumanBodyBones.LeftLowerArm
        );

        originalLeftArmRotation = leftLowerArm.localRotation;

        Debug.Log("Left lower arm found: " + leftLowerArm);
    }

    public void UpdateMotion(MotionData motion)
    {
        if (leftLowerArm == null)
            return;

        float elbowAngle = motion.pose.left_elbow;

        float bend = Mathf.InverseLerp(180f, 30f, elbowAngle);
        float rotation = Mathf.Lerp(0f, -90f, bend);

        leftLowerArm.localRotation =
            originalLeftArmRotation *
            Quaternion.Euler(rotation, 0f, 0f);
    }
}