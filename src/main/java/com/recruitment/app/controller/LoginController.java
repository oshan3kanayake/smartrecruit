package com.recruitment.app.controller;

import com.recruitment.app.model.Job;
import com.recruitment.app.model.User;
import com.recruitment.app.repository.JobRepository;
import com.recruitment.app.repository.UserRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class LoginController {

    @Autowired private UserRepository userRepository;
    @Autowired private JobRepository jobRepository;

    @GetMapping("/")
    public String home(HttpSession session, Model model) {
        User user = (User) session.getAttribute("currentUser");
        if (user != null) model.addAttribute("user", user);
        return "index";
    }

    // NOTE: /jobs and /search moved to JobController to fix the crash!

    @GetMapping("/login")
    public String showLoginPage(HttpSession session) {
        User user = (User) session.getAttribute("currentUser");
        if (user != null) return "HR".equalsIgnoreCase(user.getRole()) ? "redirect:/hr-profile" : "redirect:/jobs";
        return "login";
    }

    @PostMapping("/login")
    public String processLogin(String username, String password, HttpSession session) {
        // Warning: Add password check logic here later if needed
        User user = userRepository.findByEmail(username);
        if (user != null) {
            session.setAttribute("currentUser", user);
            if (user.getRole() != null && user.getRole().trim().equalsIgnoreCase("HR")) {
                return "redirect:/hr-profile";
            }
            return "redirect:/jobs";
        }
        return "redirect:/login?error";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/";
    }

    @GetMapping("/register")
    public String showRegisterPage(Model model) {
        model.addAttribute("user", new User());
        return "register";
    }

    @PostMapping("/register")
    public String registerUser(@ModelAttribute User user) {
        User existing = userRepository.findByEmail(user.getEmail());
        if (existing != null) {
            return "redirect:/register?error";
        }
        if (user.getRole() == null) user.setRole("CANDIDATE");
        userRepository.save(user);
        return "redirect:/login";
    }

    @GetMapping("/hr-profile")
    public String showHrProfile(Model model, HttpSession session) {
        User currentUser = (User) session.getAttribute("currentUser");
        if (currentUser == null) return "redirect:/login";
        model.addAttribute("user", currentUser);
        model.addAttribute("jobs", jobRepository.findByPostedById(currentUser.getId()));
        return "hr-profile";
    }
}