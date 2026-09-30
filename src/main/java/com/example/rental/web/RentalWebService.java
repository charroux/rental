

package com.example.rental;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.rental.service.RentallService;

/**
 * RentalWebService
 */
@RestController
public class RentalWebService {

    RentallService rentalService = new RentallService();

    // ...


    @GetMapping("/hello")
    public String sayHelle(){
        return "Hello";
    }        
}