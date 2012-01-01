<?php

class fancy_product extends simpleProduct {
    
    function __construct()
    {
        parent::__construct();
        return true;
    }
    
    
    
}


/**
 * Things wrong;
 * 
 * - inconsistent class naming 
 * - returning value from constructor
 * - unrequired constructor
 * - 
 */

?>