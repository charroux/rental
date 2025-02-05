package com.example.rent.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RentalService {

    @GetMapping("/bonjour")
    public String disBonjour(){
        return "Bonjour";
    }

}
