// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library SafeMath {
    // Custom errors for better gas efficiency
    error Overflow();
    error Underflow();
    error DivisionByZero();
    error ModulusByZero();

    /**
     * @dev Returns the addition of two unsigned integers, reverting on overflow.
     */
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (c < a) revert Overflow();
        return c;
    }

    /**
     * @dev Returns the subtraction of two unsigned integers, reverting on underflow.
     */
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (b > a) revert Underflow();
        return a - b;
    }

    /**
     * @dev Returns the multiplication of two unsigned integers, reverting on overflow.
     */
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) return 0; // Prevent multiplication by zero
        uint256 c = a * b;
        if (c / a != b) revert Overflow();
        return c;
    }

    /**
     * @dev Returns the integer division of two unsigned integers, reverting on division by zero.
     */
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        if (b == 0) revert DivisionByZero();
        return a / b;
    }

    /**
     * @dev Returns the modulus of two unsigned integers, reverting on modulus by zero.
     */
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        if (b == 0) revert ModulusByZero();
        return a % b;
    }

    /**
     * @dev Returns the exponentiation of a base to an exponent, reverting on overflow.
     */
    function pow(uint256 base, uint256 exponent) internal pure returns (uint256) {
        if (exponent == 0) return 1; // Any number to the power of 0 is 1
        uint256 result = 1;
        for (uint256 i = 0; i < exponent; i++) {
            result = mul(result, base);
        }
        return result;
    }
}
